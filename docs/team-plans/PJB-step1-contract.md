# PJB Step 1 기능 계약서 — 포인트 · 출석 · 홍보

> PJB.md Step 1 완료 조건에 대한 확정 사항 문서.
> 이 문서가 구현의 기준이 된다.

---

## 1. API 응답 필드

### GET /users/me/points/balance

```json
{
  "user_id": int,
  "current_points": int,
  "total_earned": int,
  "total_used": int
}
```

- `current_points`: 헤더 전역 잔액 표시에 사용
- `total_earned`: `point_logs`에서 `amount > 0` 합산 (백엔드 집계)
- `total_used`: `point_logs`에서 `amount < 0` 절댓값 합산 (백엔드 집계)
- 마이페이지에서 세 필드 모두 사용, 헤더는 `current_points`만 사용

---

### POST /users/me/points/logs

- 메서드 POST는 의도된 설계
- QueryParam: `page: int`, `limit: int` (기본 20)

```json
{
  "items": [
    {
      "log_id": int,
      "amount": int,
      "reason": string,
      "current_point": int,
      "updated_at": datetime
    }
  ],
  "total": int,
  "page": int,
  "limit": int
}
```

---

### GET /users/me/missions/attendance

```json
{
  "today_attended": bool,
  "streak_days": int,
  "attended_date": "string | null"
}
```

---

### POST /users/me/missions/attendance

```json
{
  "granted_points": int,
  "bonus_points": int,
  "total_granted": int,
  "current_points": int,
  "streak_days": int
}
```

- `bonus_points`: 연속 출석 보너스 (+200). 해당 없으면 0
- `total_granted`: `granted_points + bonus_points`

---

### GET /promotion-products

```json
{
  "items": [
    {
      "promo_product_id": int,
      "promo_name": string,
      "price": int,
      "duration_days": int,
      "placement": string,
      "slot_limit": int,
      "remaining_slots": int,
      "is_available": bool
    }
  ],
  "total": int
}
```

---

### GET /promotion-products/{promotion_product_id}

```json
{
  "promo_product_id": int,
  "promo_name": string,
  "price": int,
  "duration_days": int,
  "placement": string,
  "slot_limit": int,
  "remaining_slots": int,
  "is_available": bool
}
```

---

### POST /promotions

**Request**

```json
{ "promo_product_id": int, "service_id": int }
```

**Response**

```json
{
  "promotion_id": int,
  "promo_name": string,
  "service_id": int,
  "start_at": datetime,
  "end_at": datetime,
  "status": string,
  "used_points": int,
  "current_points": int
}
```

---

## 2. 빡낌 지급/차감 정책

| 시점 | 변동량 | 일일 제한 | 처리 위치 |
|---|---|---|---|
| 최초 가입 | +500 | - | User API |
| 피드백 approved | +200 | 3회 | Feedback API |
| 서비스 첫 피드백 | +300 | - | Feedback API (위 200과 중첩 가능) |
| 데일리 출석 | +100 | 1회 | POST /users/me/missions/attendance |
| 7 / 15 / 30일 연속 출석 달성 | +200 | - | POST /users/me/missions/attendance |
| 홍보 신청 | -상품 가격 | - | POST /promotions |

> 모든 지급/차감: `point_logs INSERT + users.current_points UPDATE` 단일 트랜잭션

---

## 3. 출석 정책

| 항목 | 기준 |
|---|---|
| 날짜 기준 | KST |
| 하루 제한 | 1회 (중복 시 400) |
| 연속 초기화 | 하루라도 빠지면 `streak_count = 1` |
| 연속 보너스 | 7일 / 15일 / 30일 달성 시 +200 (기본 +100 별도) |

---

## 4. 홍보 정책

### 상품 가격표 (최최종 확정)

| 상품명 | 가격 | 슬롯 | duration_days |
|---|---|---|---|
| 홈 화면 크게 노출 | 5,000 | 5 | 1 |
| 상단 배너 | 4,000 | 10 | 1 |
| 추천 서비스 | 3,000 | 5 | 1 |
| 서비스 카드 | 1,500 | 20 | 1 |
| 팝업 | 1,000 | 5 | 1 |

> 1차 배포: 모든 상품 `duration_days = 1`, `is_active = true`

### 슬롯 관리

- `promotion_products.slot_limit` 기준
- `remaining_slots = slot_limit - COUNT(promotions WHERE promo_product_id = ? AND status = '진행중' AND end_at > NOW())`
- 동시 신청: `SELECT FOR UPDATE`로 선착순 처리
- 슬롯 소진 시 409 반환

### 만료 처리

- 스케줄러 없음
- 조회 시점에 `AND end_at > NOW()` 조건으로 만료 판단
- DB `status` 컬럼은 업데이트하지 않음

### 중복 신청 차단

- 드롭다운에서 이미 홍보 중인 서비스 선택 불가 (사전 차단)
- 모달 열릴 때 `GET /users/me/promotions/active` 호출 → 활성 서비스 목록 확인
- 서버 409: 최후 방어선

### 홍보 노출 데이터

- `services.title`, `services.summary`, `services.thumbnail_url`, `services.service_url` 재사용
- 별도 소재 업로드 없음

---

## 5. TABLE_DEF 변경 사항

| 테이블 | 항목 | 변경 내용 |
|---|---|---|
| `feedbacks` | `service_id` FK | `products(product_id)` → `services(service_id)` |
| `promotions` | `service_id` FK | `products(product_id)` → `services(service_id)` |
| `community_comments` | `post_id` FK | `community_posts(c_post_id)` → `community_posts(post_id)` |
| `point_logs` | `current_point` CHECK | `(balance >= 0)` → `(current_point >= 0)` |
| `user_follows` | UNIQUE | `follower_id`, `following_id` 단독 UNIQUE → 복합 UNIQUE `(follower_id, following_id)` |
| `attendance` | `streak_count` | `INT NOT NULL DEFAULT 1` 추가 |
| `promotion_products` | `placement` | `VARCHAR NOT NULL` 추가 |
| `promotion_products` | `slot_limit` | `INT NOT NULL CHECK (slot_limit > 0)` 추가 |
| `promotion_products` | `is_active` | `BOOLEAN NOT NULL DEFAULT true` 추가 |
