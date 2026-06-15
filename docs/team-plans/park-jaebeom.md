# 박재범 작업 계획: 포인트 관련 기능 전체

## 목표

BuildBack의 내부 포인트인 빡낌을 정확히 지급, 차감, 조회할 수 있는 공통 포인트 시스템을 만든다. 모든 포인트 증감은 원장에 기록되어야 하며, 홍보 구매와 미션 보상까지 같은 규칙으로 처리한다.

## 담당 기능

- 포인트 잔액 관리 
- 포인트 원장
- 최초 가입 보상
- 피드백 작성 보상
- 서비스의 첫 피드백 추가 보상
- 데일리 출석 보상
- 7일/15일/30일 연속 출석 보상
- 홍보 상품 구매 차감
- 홍보 슬롯 선착순 구매 처리
- 포인트 이력 조회

## 구현 범위

### 포인트 지급 정책

| 조건 | 지급량 |
| --- | ---: |
| 최초 가입 | 500 빡낌 |
| 피드백 작성 | 200 빡낌 |
| 서비스의 첫 피드백 작성 | 추가 300 빡낌 |
| 데일리 출석 | 100 빡낌 |
| 7일 연속 출석 | 추가 200 빡낌 |
| 15일 연속 출석 | 추가 200 빡낌 |
| 30일 연속 출석 | 추가 200 빡낌 |

### 포인트 차감 정책

| 사용처 | 차감량 |
| --- | ---: |
| 홈 화면 크게 노출 | 5000 빡낌 |
| 상단 배너 | 3000 빡낌 |
| 접속 시 팝업 | 2000 빡낌 |

잔액이 부족하면 구매를 차단한다.

### 포인트 원장

모든 지급과 차감은 `point_transactions`에 먼저 기록하고, 사용자 잔액을 함께 갱신한다.

중복 지급 방지를 위해 `reason`, `related_type`, `related_id`, `user_id` 조합의 멱등성을 보장한다.

예시:

- 같은 회원에게 최초 가입 보상은 1회만 지급
- 같은 피드백에 대한 작성 보상은 1회만 지급
- 같은 날짜 출석 보상은 1회만 지급
- 같은 연속 출석 달성 보상은 1회만 지급

### 출석 미션

하루 기준은 KST 날짜다.

처리 순서:

1. 오늘 이미 출석했는지 확인
2. 어제 출석 여부로 연속 출석 계산
3. 데일리 보상 지급
4. 7일/15일/30일 달성 여부 확인
5. 달성 보상 지급
6. 출석 기록 저장

### 홍보 구매

홍보 상품:

- 홈 화면 크게 노출: 5000 빡낌, 5개 슬롯
- 상단 배너: 3000 빡낌, 10개 슬롯
- 접속 시 팝업: 2000 빡낌

구매 처리 순서:

1. 상품 활성 여부 확인
2. 잔여 슬롯 확인
3. 사용자 잔액 확인
4. 포인트 차감
5. 홍보 슬롯 생성
6. 구매 결과 반환

동시 구매가 발생할 수 있으므로 슬롯 확인과 포인트 차감은 트랜잭션으로 묶는다.

## 데이터 모델

### point_transactions

- id
- user_id
- amount
- balance_after
- reason
- related_type
- related_id
- created_at

### attendances

- id
- user_id
- attendance_date
- streak_count
- reward_amount
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

## API 초안

- `GET /api/me/points`
- `GET /api/me/point-transactions`
- `POST /api/points/reward/signup`
- `POST /api/points/reward/feedback`
- `GET /api/missions/me`
- `POST /api/missions/attendance`
- `GET /api/promotions/products`
- `GET /api/promotions/active`
- `POST /api/promotions/purchase`

내부 서비스 함수:

- `grantPoints(userId, amount, reason, relatedType, relatedId)`
- `spendPoints(userId, amount, reason, relatedType, relatedId)`
- `getPointBalance(userId)`
- `assertIdempotentReward(userId, reason, relatedType, relatedId)`

## 다른 담당자와 맞출 부분

- 김현진: 최초 가입 이벤트, 피드백 품질 검사 통과 이벤트
- 조현정: 홍보 구매 대상 서비스와 활성 홍보 노출
- 김은경: 마이페이지 포인트 잔액과 최근 이력
- 박건일: 신고로 인한 수동 회수 정책이 필요한지 결정

## 완료 기준

- 최초 가입 보상이 중복 없이 지급된다.
- 피드백 작성 보상과 첫 피드백 추가 보상이 정확히 지급된다.
- 일일 피드백 보상은 3회까지만 지급된다.
- 데일리 출석과 연속 출석 보상이 KST 기준으로 지급된다.
- 홍보 구매 시 잔액과 슬롯이 검증되고 포인트가 차감된다.
- 모든 포인트 증감 이력이 원장에 남는다.
- 마이페이지에서 보이는 잔액과 원장 합계가 일치한다.
