# 김현진 작업 계획: 피드백, 소셜 로그인, 최초 관심분야 입력

## 목표

사용자가 구글 계정으로 쉽게 가입하고, 최초 관심분야를 입력한 뒤, 다른 서비스에 품질 있는 피드백을 남길 수 있는 핵심 흐름을 만든다.

## 담당 기능 

- 구글 소셜 로그인
- 회원 생성 및 세션 관리
- 최초 로그인 여부 판단
- 관심분야 선택/건너뛰기
- 관심분야 기반 서비스 5개 랜덤 추천
- 피드백 작성/수정/삭제 제한
- 피드백 품질 LLM 검사
- 피드백 일일 3회 제한

## 구현 범위

### 구글 로그인

구글 OAuth만 지원한다.

회원 생성 시 저장할 핵심 필드:

- oauth_provider
- oauth_id
- email
- nickname
- avatar_url
- point_balance
- joined_at
- last_login_at

최초 가입 여부를 명확히 반환해야 박재범 담당 포인트 기능에서 최초 가입 보상을 중복 없이 지급할 수 있다.

### 최초 관심분야 입력

최초 로그인 사용자는 관심분야 화면으로 이동한다.

- 선택은 선택사항이다.
- 선택하지 않고 건너뛸 수 있다.
- 여러 개 선택 가능 여부는 UI 복잡도를 줄이기 위해 1차 배포에서는 최대 3개로 제한한다.
- 선택 완료 후 해당 카테고리 서비스 5개를 랜덤 추천한다.
- 선택값이 없거나 해당 카테고리에 서비스가 없으면 전체 서비스 랜덤 추천으로 대체한다.

### 피드백 작성

정책:

- 본인 서비스에는 작성 불가
- 같은 서비스에 사용자당 1개만 작성 가능
- 하루 최대 3개 작성 가능
- 품질 검사 통과 시에만 저장 또는 승인
- 작성 후 30일 이내 삭제 불가
- 수정 시에도 품질 검사 재실행

### 피드백 품질 LLM 검사

검사 기준:

- 실제 사용 경험이 드러나는가
- 장점 또는 불편한 점이 구체적인가
- 서비스와 관련 있는 내용인가
- 욕설, 비방, 스팸, 복붙성 내용이 아닌가

검사 결과는 `approved`, `rejected`, `needs_revision` 중 하나로 저장한다.

## 데이터 모델

### users

- id
- oauth_provider
- oauth_id
- email
- nickname
- avatar_url
- point_balance
- joined_at
- last_login_at
- onboarding_completed_at
- is_banned

### user_interests

- id
- user_id
- category_id
- created_at

### feedbacks

- id
- service_id
- author_user_id
- content
- quality_status
- quality_score
- quality_reason
- created_at
- updated_at
- deleted_at

## API 초안

- `GET /api/auth/google/start`
- `GET /api/auth/google/callback`
- `POST /api/auth/logout`
- `GET /api/me`
- `GET /api/categories`
- `POST /api/me/interests`
- `POST /api/me/onboarding/skip`
- `GET /api/recommendations/initial`
- `POST /api/services/:id/feedbacks`
- `PATCH /api/feedbacks/:id`
- `DELETE /api/feedbacks/:id`
- `GET /api/me/feedback-quota`

## 다른 담당자와 맞출 부분

- 박재범: 최초 가입, 피드백 작성, 첫 피드백 보상 지급 이벤트
- 조현정: 서비스 등록 조건에 필요한 피드백 작성 여부
- 김은경: 마이페이지의 내 피드백 목록
- 박건일: 신고된 서비스/글/댓글 작성자의 제재 상태가 피드백 작성 권한에 미치는 영향

## 완료 기준

- 구글 로그인 후 회원이 생성되고 세션이 유지된다.
- 최초 로그인 사용자가 관심분야를 선택하거나 건너뛸 수 있다.
- 관심분야 기반 추천 서비스가 최대 5개 노출된다.
- 사용자가 정책 조건을 만족할 때만 피드백을 작성할 수 있다.
- 피드백 작성/수정 시 LLM 품질 검사가 실행된다.
- 피드백 일일 3회 제한이 동작한다.
