# BuildBack AI 모델 고도화 및 데이터 수집 설계

> 목적: 1차 배포 이후 추가할 AI 기능을 `피드백 매칭 추천 모델`과 `피드백 품질 점수 예측 모델` 두 가지로 좁히고, 1차 운영 단계부터 어떤 데이터를 어떤 구조로 모아야 하는지 정리한다.

## 1. 집중할 AI 기능

BuildBack의 1차 배포 목적은 피드백 품앗이 루프가 실제로 작동하는지 검증하는 것이다. 이후 AI 고도화는 이 루프를 더 잘 돌게 만드는 두 기능에 집중한다.

| 기능 | 목표 |
| --- | --- |
| 피드백 매칭 추천 모델 | 내 서비스에 구체적이고 도움 되는 피드백을 남길 가능성이 높은 사용자를 추천한다. |
| 피드백 품질 점수 예측 모델 | 작성된 피드백이 실제 사용 경험과 개선 제안을 충분히 담고 있는지 점수화한다. |

두 모델은 서로 연결된다. 품질 점수 예측 모델이 각 사용자의 피드백 품질 이력을 만들고, 피드백 매칭 추천 모델은 그 이력을 활용해 서비스별로 좋은 리뷰어를 추천한다.

```text
피드백 작성
    ↓
피드백 품질 점수 예측
    ↓
사용자별/카테고리별 피드백 신뢰도 축적
    ↓
피드백 매칭 추천 모델 개선
    ↓
서비스별 좋은 리뷰어 추천
```

## 2. 공통 데이터 수집 원칙

- 원본 텍스트와 AI 분석 결과는 분리해서 저장한다.
- 추천, 노출, 클릭, 피드백 작성 같은 행동은 이벤트 로그로 남긴다.
- AI 판단 결과에는 `model_name`, `model_version`, `prompt_version`, `created_at`을 함께 저장한다.
- 피드백 품질 검사의 통과/실패뿐 아니라 점수와 사유 코드를 저장한다.
- 사용자가 선택한 관심분야와 실제 행동 기반 관심분야를 구분해서 저장한다.
- 이메일, OAuth ID, 원본 IP 등 개인 식별 정보는 모델 학습 데이터에서 제외하거나 익명화한다.

## 3. 피드백 매칭 추천 모델

### 3.1 기능 정의

피드백 매칭 추천 모델은 특정 서비스에 대해 “누가 좋은 피드백을 남길 가능성이 높은가”를 예측한다.

활용 화면:

- 서비스 제작자용 “피드백 요청 추천 대상”
- 홈/서비스 목록의 개인화 노출
- 피드백이 부족한 서비스와 활동적인 리뷰어 매칭
- 카테고리별 고품질 리뷰어 추천

예시:

```text
서비스: AI 기반 웹소설 추천 서비스

추천 리뷰어:
1. 콘텐츠 카테고리 피드백 품질 평균이 높은 사용자
2. AI 서비스에 자주 피드백을 남긴 사용자
3. 최근 7일 내 활동했고 피드백 수락률이 높은 사용자
```

### 3.2 모델이 예측해야 할 값

| 예측값 | 설명 |
| --- | --- |
| feedback_probability | 해당 사용자가 이 서비스에 피드백을 남길 가능성 |
| quality_expected_score | 남긴다면 품질 높은 피드백일 가능성 |
| relevance_score | 사용자 관심사와 서비스 주제의 적합도 |
| activity_score | 최근 활동성과 응답 가능성 |
| abuse_risk_score | 포인트 목적의 저품질 피드백 가능성 |

최종 추천 점수는 단순히 클릭 가능성이 아니라 “피드백을 남길 가능성 × 피드백 품질 기대값”에 가깝게 설계하는 것이 좋다.

```text
matching_score =
    feedback_probability
    * quality_expected_score
    * relevance_score
    * activity_score
    - abuse_risk_penalty
```

### 3.3 필요한 데이터 구조

#### 사용자 관심 데이터

| 데이터 | 구조 |
| --- | --- |
| 선택 관심분야 | `user_id`, `category_id`, `source=onboarding`, `created_at` |
| 행동 기반 관심분야 | `user_id`, `category_id`, `view_count`, `click_count`, `feedback_count`, `last_activity_at` |
| 최근 활동 | `user_id`, `last_login_at`, `last_feedback_at`, `active_days_7d`, `active_days_30d` |
| 리뷰어 상태 | `user_id`, `is_banned`, `can_receive_match`, `created_at`, `updated_at` |

#### 서비스 데이터

| 데이터 | 구조 |
| --- | --- |
| 기본 정보 | `service_id`, `owner_user_id`, `title`, `description`, `category_id`, `url`, `status` |
| 피드백 요청 정보 | `service_id`, `feedback_goal`, `target_user`, `current_stage`, `created_at` |
| 서비스 태그 | `service_id`, `tag`, `source`, `created_at` |
| 서비스 통계 | `service_id`, `view_count`, `external_click_count`, `feedback_count`, `avg_feedback_quality_score` |

`feedback_goal`, `target_user`, `current_stage`는 1차 필수 기능이 아니어도 선택 입력으로 받는 것이 좋다. 이 값이 있으면 “누가 이 서비스에 적합한 리뷰어인가”를 훨씬 정확히 판단할 수 있다.

#### 피드백 이력 데이터

| 데이터 | 구조 |
| --- | --- |
| 작성 이력 | `feedback_id`, `author_user_id`, `service_id`, `service_category_id`, `created_at` |
| 품질 점수 | `feedback_id`, `quality_score`, `quality_labels`, `quality_reason_code`, `model_version` |
| 카테고리별 신뢰도 | `user_id`, `category_id`, `feedback_count`, `avg_quality_score`, `accepted_rate`, `updated_at` |
| 신고/거절 이력 | `user_id`, `reported_feedback_count`, `rejected_feedback_count`, `last_reported_at` |

#### 추천 학습용 이벤트 데이터

| 이벤트 | 필수 필드 |
| --- | --- |
| 추천 후보 생성 | `event_id`, `service_id`, `candidate_user_id`, `algorithm_version`, `rank`, `score`, `created_at` |
| 추천 노출 | `event_id`, `service_id`, `candidate_user_id`, `placement`, `rank`, `created_at` |
| 추천 클릭 | `event_id`, `service_id`, `candidate_user_id`, `requester_user_id`, `created_at` |
| 피드백 요청 전송 | `event_id`, `service_id`, `target_user_id`, `requester_user_id`, `created_at` |
| 피드백 요청 수락 | `event_id`, `service_id`, `target_user_id`, `created_at` |
| 피드백 작성 완료 | `event_id`, `service_id`, `target_user_id`, `feedback_id`, `created_at` |

추천 모델에는 “추천했지만 피드백을 남기지 않은 데이터”도 필요하다. 따라서 추천 노출 로그와 작성 완료 로그를 반드시 연결할 수 있어야 한다.

### 3.4 학습 라벨

피드백 매칭 추천 모델의 정답 라벨은 단일 값보다 여러 단계로 나누는 것이 좋다.

| 라벨 | 정의 |
| --- | --- |
| viewed | 추천 대상 또는 서비스가 사용자에게 노출됨 |
| clicked | 사용자가 서비스 상세 또는 URL을 클릭함 |
| started_feedback | 사용자가 피드백 작성을 시작함 |
| submitted_feedback | 사용자가 피드백을 제출함 |
| accepted_feedback | 피드백이 품질 기준을 통과함 |
| high_quality_feedback | 피드백 품질 점수가 기준 이상임 |

초기 모델은 `accepted_feedback` 또는 `high_quality_feedback`을 주요 라벨로 삼는 것이 적합하다.

## 4. 피드백 품질 점수 예측 모델

### 4.1 기능 정의

피드백 품질 점수 예측 모델은 피드백이 BuildBack의 취지에 맞는지 판단한다. 단순 감정 분석이 아니라 “서비스 개선에 실제로 도움이 되는가”를 평가해야 한다.

활용 화면:

- 피드백 등록 전 품질 검사
- 피드백 보상 지급 여부 판단
- 좋은 피드백 작성자 신뢰도 계산
- 서비스 제작자 화면에서 고품질 피드백 우선 정렬
- 피드백 매칭 추천 모델의 사용자 신뢰도 피처 생성

### 4.2 평가 기준

| 기준 | 설명 |
| --- | --- |
| 구체성 | 막연한 칭찬/비판이 아니라 구체적인 화면, 기능, 경험을 언급하는가 |
| 관련성 | 해당 서비스의 내용과 직접 관련이 있는가 |
| 사용 경험성 | 실제로 접속하거나 사용해본 흔적이 있는가 |
| 개선 가능성 | 제작자가 행동으로 옮길 수 있는 제안이 있는가 |
| 균형성 | 장점, 문제점, 제안 중 하나 이상을 의미 있게 담고 있는가 |
| 안전성 | 욕설, 비방, 혐오, 개인정보 노출, 스팸이 없는가 |

### 4.3 점수 체계

1차에서는 운영과 학습을 모두 고려해 0~100점 점수와 사유 코드를 함께 저장한다.

| 점수 구간 | 의미 | 처리 |
| --- | --- | --- |
| 0~39 | 저품질 또는 부적절 | 등록 거절 또는 수정 요청 |
| 40~69 | 최소 기준 통과 | 등록 가능, 기본 보상 |
| 70~89 | 좋은 피드백 | 등록 가능, 신뢰도 상승 |
| 90~100 | 매우 좋은 피드백 | 향후 추가 보상 후보 |

사유 코드는 최소한 아래처럼 구조화한다.

| 코드 | 의미 |
| --- | --- |
| too_short | 지나치게 짧음 |
| generic | 어느 서비스에나 붙일 수 있는 일반 문장 |
| not_related | 서비스와 직접 관련이 낮음 |
| no_usage_signal | 실제 사용 흔적이 부족함 |
| no_actionable_suggestion | 실행 가능한 개선 제안이 없음 |
| abusive | 욕설/비방/혐오 표현 포함 |
| spam_like | 복붙 또는 홍보성 문장 |
| specific_and_useful | 구체적이고 유용함 |
| balanced_feedback | 장점과 개선점이 균형 있게 포함됨 |

### 4.4 필요한 데이터 구조

#### 피드백 원본 데이터

| 데이터 | 구조 |
| --- | --- |
| 피드백 원문 | `feedback_id`, `service_id`, `author_user_id`, `content`, `created_at`, `updated_at` |
| 구조화 입력 | `feedback_id`, `positive_text`, `problem_text`, `suggestion_text`, `willingness_score` |
| 사용 맥락 | `feedback_id`, `device_type`, `used_feature`, `usage_depth`, `created_at` |
| 수정 이력 | `feedback_id`, `previous_content`, `new_content`, `changed_at` |

1차에서 자유 텍스트 하나만 받더라도, 가능하면 다음 3개 입력칸으로 분리하는 것이 좋다.

- 좋았던 점
- 불편했던 점
- 개선 제안

이 구조는 나중에 품질 점수 모델의 강한 학습 피처가 된다.

#### AI 평가 결과

| 데이터 | 구조 |
| --- | --- |
| 품질 점수 | `feedback_id`, `quality_score`, `quality_status`, `quality_reason_code`, `quality_reason_text` |
| 세부 점수 | `feedback_id`, `specificity_score`, `relevance_score`, `usage_signal_score`, `actionability_score`, `safety_score` |
| 모델 정보 | `feedback_id`, `model_name`, `model_version`, `prompt_version`, `evaluated_at` |
| 보상 결과 | `feedback_id`, `rewarded`, `reward_amount`, `reward_reason`, `created_at` |

#### 운영자 라벨 데이터

| 데이터 | 구조 |
| --- | --- |
| 운영자 판정 | `feedback_id`, `admin_label`, `admin_reason_code`, `admin_id`, `reviewed_at` |
| 이의/수정 결과 | `feedback_id`, `previous_status`, `new_status`, `changed_by`, `changed_at` |
| 샘플링 여부 | `feedback_id`, `sampled_for_training`, `sample_reason`, `created_at` |

운영자 라벨은 많지 않아도 된다. 다만 모델 품질을 올리려면 좋은 피드백과 나쁜 피드백 샘플을 꾸준히 모아야 한다.

### 4.5 학습 라벨

| 라벨 | 정의 |
| --- | --- |
| pass_fail | 품질 기준 통과 여부 |
| quality_score | 0~100 품질 점수 |
| reason_codes | 품질 판단 사유 코드 목록 |
| admin_label | 운영자가 최종 판단한 라벨 |
| owner_helpful | 서비스 제작자가 도움이 되었다고 표시했는지 여부 |

가장 가치 있는 라벨은 `owner_helpful`이다. 서비스 제작자가 “이 피드백이 실제로 도움이 됐다”고 표시한 데이터는 품질 모델과 매칭 모델 모두에 강한 신호가 된다.

## 5. 1차 배포 때 바로 반영할 데이터 모델 보강

### 5.1 feedbacks 보강

기존 `feedbacks`에 아래 필드를 추가하거나 별도 평가 테이블로 분리한다.

```text
quality_score
quality_status
quality_reason_code
quality_reason_text
rewarded
reward_amount
evaluated_model_version
```

### 5.2 feedback_quality_evaluations

AI 평가 이력을 남기기 위한 테이블이다. 같은 피드백을 다른 모델이나 프롬프트로 다시 평가할 수 있어야 한다.

```text
id
feedback_id
quality_score
quality_status
reason_codes
detail_scores_json
model_name
model_version
prompt_version
input_snapshot_json
output_json
created_at
```

### 5.3 user_category_feedback_stats

피드백 매칭 추천 모델에서 사용할 사용자별 카테고리 신뢰도 테이블이다.

```text
id
user_id
category_id
feedback_count
accepted_feedback_count
high_quality_feedback_count
avg_quality_score
reported_feedback_count
last_feedback_at
updated_at
```

### 5.4 event_logs

추천 모델 학습에 필요한 공통 이벤트 테이블이다.

```text
id
user_id
event_type
target_type
target_id
source
metadata_json
created_at
```

필수 `event_type`:

- `service_impression`
- `service_click`
- `external_url_click`
- `feedback_start`
- `feedback_submit`
- `reviewer_recommendation_impression`
- `reviewer_recommendation_click`
- `feedback_request_sent`
- `feedback_request_accepted`

### 5.5 reviewer_recommendation_logs

피드백 매칭 추천 결과를 학습하기 위한 테이블이다.

```text
id
service_id
requester_user_id
candidate_user_id
rank
matching_score
score_components_json
algorithm_version
impressed_at
clicked_at
requested_at
accepted_at
feedback_id
created_at
```

## 6. 1차에서 최소로 수집해야 할 데이터

### 필수

- 사용자 관심분야
- 서비스 제목, 설명, 카테고리, URL
- 피드백 원문
- 피드백 품질 점수, 통과 여부, 사유 코드
- 피드백 보상 여부와 보상량
- 사용자별 카테고리 피드백 수와 평균 품질 점수
- 서비스 노출, 클릭, 외부 URL 클릭
- 피드백 작성 시작, 제출 완료
- 추천 노출, 추천 클릭

### 가능하면 추가

- 서비스 제작자가 받고 싶은 피드백 주제
- 서비스의 목표 사용자
- 서비스 현재 단계: 아이디어, MVP, 베타, 운영 중
- 피드백의 좋았던 점/불편했던 점/개선 제안 분리 입력
- 제작자의 `도움됨` 표시
- 운영자 샘플 라벨

## 7. 개발 우선순위

### 1단계: 품질 점수 예측 기반 데이터 축적

- 피드백 작성 시 LLM 품질 검사 실행
- `quality_score`, `quality_status`, `reason_codes` 저장
- 피드백 보상 지급 여부와 연결
- 사용자별 평균 품질 점수 집계

### 2단계: 규칙 기반 피드백 매칭 추천

초기에는 머신러닝 모델 없이 규칙 기반으로 시작한다.

추천 기준:

- 서비스 카테고리와 사용자 관심분야 일치
- 해당 카테고리 피드백 품질 평균
- 최근 활동 여부
- 신고/거절 이력
- 같은 서비스에 이미 피드백을 남겼는지 여부

### 3단계: 학습 기반 매칭 모델

추천 노출, 클릭, 요청, 피드백 제출, 품질 점수 데이터가 쌓이면 학습 기반 모델로 전환한다.

목표 라벨:

- `submitted_feedback`
- `accepted_feedback`
- `high_quality_feedback`
- `owner_helpful`

### 4단계: 두 모델 연동

피드백 품질 점수 예측 모델의 결과를 리뷰어별 신뢰도 피처로 만들고, 피드백 매칭 추천 모델의 입력값으로 사용한다.

## 8. 결론

BuildBack의 AI 고도화는 많은 기능을 한 번에 붙이는 것보다 아래 두 모델을 깊게 만드는 편이 제품 핵심 루프에 더 직접적으로 기여한다.

- 피드백 매칭 추천 모델: 좋은 피드백을 줄 사람을 서비스에 연결한다.
- 피드백 품질 점수 예측 모델: 피드백의 질을 측정하고 좋은 리뷰어 데이터를 만든다.

따라서 1차 배포부터 가장 중요한 것은 피드백 원문, 품질 점수, 사용자별 카테고리 신뢰도, 추천 노출/반응 이벤트를 구조화해서 남기는 것이다. 이 데이터가 쌓이면 BuildBack은 단순한 품앗이 플랫폼에서 “좋은 피드백이 필요한 서비스와 좋은 피드백을 줄 사람을 연결하는 플랫폼”으로 고도화할 수 있다.
