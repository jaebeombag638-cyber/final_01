# BuildBack 1차 배포 PLAN

> 목표: 완성형 AI 서비스가 아니라, 빌더들이 실제로 가입하고 서비스를 등록하며 서로 피드백을 남기는 핵심 순환 구조를 빠르게 검증한다.

## 1. 1차 배포 목적

BuildBack의 장기 비전은 초보 빌더들이 서로의 첫 사용자가 되어주고, 피드백과 성장 과정을 기반으로 서비스 개선을 이어가는 공개 성장 플랫폼이다.

1차 배포에서는 AI 분석, 프로젝트 성장 일지, 팔로우, 고도화된 추천 기능보다 다음 루프가 실제로 작동하는지 검증한다.

```text
구글 로그인
    ↓
관심분야 선택
    ↓
다른 서비스 탐색
    ↓
피드백 작성
    ↓
빡낌 획득
    ↓
내 서비스 등록
    ↓
홍보 슬롯 구매
    ↓
피드백 수집
```

핵심 지표는 "가입자가 실제 피드백을 남기는가", "피드백을 남긴 사용자가 자신의 서비스를 등록하는가", "빡낌을 홍보에 사용하는가"이다.


## 2. 사용할 공통 테이블

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
- is_banned

### user_interests

- id
- user_id
- category_id
- created_at

### categories

- id
- name
- slug
- sort_order
- is_active

### services

- id
- owner_user_id
- category_id
- title
- description
- url
- url_risk_status
- status
- created_at
- updated_at

### feedbacks

- id
- service_id
- author_user_id
- content
- quality_status
- quality_reason
- created_at
- updated_at
- deleted_at

### point_transactions

- id
- user_id
- amount
- reason
- related_type
- related_id
- created_at

### promotion_products

- id
- name
- price
- slot_limit
- duration_hours
- placement
- is_active

### promotions

- id
- service_id
- buyer_user_id
- product_id
- starts_at
- ends_at
- status
- created_at

### attendances

- id
- user_id
- attendance_date
- streak_count
- reward_amount
- created_at

### community_posts

- id
- board_type
- author_user_id
- title
- content
- status
- created_at
- updated_at

### reports

- id
- reporter_user_id
- target_type
- target_id
- reason
- detail
- status
- created_at
- resolved_at


## 3. 데이터 수집 목표

1차 배포의 진짜 목적은 완성된 기능이 아니라 향후 AI 기능을 위한 실제 데이터를 모으는 것이다.


## 4. 1차 배포 완료 기준

다음 조건을 만족하면 1차 배포 가능 상태로 본다.

- 사용자가 구글 로그인으로 가입할 수 있다.
- 최초 로그인 사용자가 관심분야를 선택하거나 건너뛸 수 있다.
- 관심분야 기반 추천 서비스가 노출된다.
- 사용자가 조건 충족 후 서비스를 등록할 수 있다.
- 등록 URL이 Web Risk API로 검사된다.
- 사용자가 다른 서비스에 피드백을 작성할 수 있다.
- 피드백 작성 시 LLM 품질 검사가 실행된다.
- 피드백 보상과 첫 피드백 보상이 지급된다.
- 출석 보상이 지급된다.
- 사용자가 빡낌으로 홍보 슬롯을 구매할 수 있다.
- 홍보 구매 즉시 홈/배너/팝업 노출에 반영된다.
- 커뮤니티 게시글을 작성할 수 있다.
- 커뮤니티 글 작성 시 키워드 필터링이 동작한다.
- 서비스와 커뮤니티 글을 신고할 수 있다.
- 관리자 또는 운영자가 신고 대상과 포인트 이력을 확인할 수 있다.
