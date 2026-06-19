# PJB Step 1 기능 계약서 — 포인트 · 출석 · 홍보

> PJB.md Step 1 완료 조건에 대한 확정 사항 문서.
> 이 문서가 구현의 기준이 된다.

---

## 1. API 응답 필드

### GET /users/me/points/balance

**언제 씀:** 헤더 렌더링 시, 빡낌 변동(출석·피드백·홍보 신청) 직후 재조회

```json
{
  "user_id": int,
  "current_points": int,
  "total_earned": int,
  "total_used": int
}
```

| 필드 | 설명 |
|---|---|
| `current_points` | 현재 보유 빡낌. `users.current_points` DB 컬럼에서 읽음. 빡낌 변동 시 `point_logs INSERT + users.current_points UPDATE` 트랜잭션으로 항상 동기화. 헤더에 표시 |
| `total_earned` | 지금까지 받은 빡낌 총합 (`amount > 0` 합산). 마이페이지에 표시 |
| `total_used` | 지금까지 쓴 빡낌 총합 (`amount < 0` 절댓값 합산). 마이페이지에 표시 |

---

### GET /users/me/points/logs

**언제 씀:** 마이페이지 → 내 빡낌 → 자세히 보기에서 변동 내역 페이지네이션 조회

- QueryParam: `page: int`, `limit: int` (기본 20)
- 정렬: `ORDER BY updated_at DESC` (최신순 고정)

```json
{
  "items": [
    {
      "log_id": int,
      "amount": int,
      "reason": string,
      "current_points": int,
      "updated_at": datetime
    }
  ],
  "total": int,
  "page": int,
  "limit": int
}
```

| 필드 | 설명 |
|---|---|
| `amount` | 양수면 지급, 음수면 차감. 예: `+100`, `-3000` |
| `reason` | 변동 사유. `"출석"` / `"연속출석보너스"` / `"피드백"` / `"서비스 첫 피드백"` / `"홍보 신청"` / `"가입 보상"` |
| `current_points` | 이 변동 이후의 잔액 스냅샷 (예: 차감 후 남은 빡낌) |
| `updated_at` | KST 기준 변동 시각 |

> 로그는 수정·삭제 불가. 피드백 삭제 시에도 지급 로그 유지.
> `updated_at`은 DB 컬럼명 그대로 사용. "사용자 포인트 상태가 변동된 시각"을 의미하며, 로그 레코드 자체가 수정됨을 뜻하지 않는다.

---

### GET /users/me/missions/attendance

**언제 씀:** 마이페이지 진입 시 출석 버튼 상태와 연속 출석일 표시용

```json
{
  "today_attended": bool,
  "streak_days": int,
  "attended_date": "string | null"
}
```

| 필드 | 설명 |
|---|---|
| `today_attended` | `true`면 오늘 이미 출석 → 출석 버튼 비활성화 |
| `streak_days` | 현재 연속 출석일 수. 버튼 아래 "연속 N일 출석 중" 표시용. 연속이 끊기고 오늘 아직 미출석이면 `0` |
| `attended_date` | 마지막 출석 날짜. 한 번도 출석 안 했으면 `null` |

---

### POST /users/me/missions/attendance

**언제 씀:** 출석 버튼 클릭 시 호출. 성공 시 토스트 표시용 데이터 반환

```json
{
  "granted_points": int,
  "bonus_points": int,
  "total_granted": int,
  "current_points": int,
  "streak_days": int
}
```

| 필드 | 설명 |
|---|---|
| `granted_points` | 기본 출석 지급량 (+100 고정) |
| `bonus_points` | 7·15·30일 연속 달성 시 +200, 해당 없으면 0 |
| `total_granted` | `granted_points + bonus_points`. 토스트에 "오늘 받은 빡낌 N" 표시용 |
| `current_points` | 지급 후 잔액. 헤더 즉시 갱신에 사용 |
| `streak_days` | 갱신된 연속 출석일 수. 버튼 아래 문구 즉시 갱신용 |

> 오늘 이미 출석한 상태에서 재요청 시 400 반환.

---

### `attendance.streak_count` 컬럼 구조와 읽기/쓰기 방식

**변경 전 → 변경 후**

```
변경 전                          변경 후
┌───────────┬───────────────┐   ┌───────────┬───────────────┬──────────────┐
│ attend_id │ attended_date │   │ attend_id │ attended_date │ streak_count │
├───────────┼───────────────┤   ├───────────┼───────────────┼──────────────┤
│ 1         │ 2026-06-15    │   │ 1         │ 2026-06-15    │ 1            │
│ 2         │ 2026-06-16    │   │ 2         │ 2026-06-16    │ 2            │
│ 3         │ 2026-06-17    │   │ 3         │ 2026-06-17    │ 3            │
│ 4         │ 2026-06-19    │   │ 4         │ 2026-06-19    │ 1  ← 하루 건너뜀, 리셋
└───────────┴───────────────┘   └───────────┴───────────────┴──────────────┘
```

> **[Step 2 / Step 3]** — 읽기·쓰기 구현 방식. 조회는 Step 2, 출석 처리는 Step 3에서 구현

**쓰는 방식**

- **POST /attendance (출석할 때):** 백엔드가 직전 행의 `attended_date`를 보고 streak 계산 후 INSERT
  - 어제 출석 O → `streak_count = 직전 행 + 1`
  - 어제 출석 X → `streak_count = 1` (리셋)
- **GET /attendance (조회할 때):** `ORDER BY attend_id DESC LIMIT 1`로 최근 행을 읽은 뒤 `attended_date`가 어제 이내인지 확인
  - `attended_date`가 오늘 또는 어제(KST) → 최근 행의 `streak_count` 그대로 반환
  - `attended_date`가 그 이전 → `streak_days = 0` 반환 (연속이 끊겼고 오늘 미출석)

> 쓸 때 계산 한 번, 읽을 때 `attended_date` 어제 이내 여부만 추가 확인.

---

### GET /promotion-products

**언제 씀:** 홍보 상품 목록 화면 진입 시

```json
{
  "items": [
    {
      "promo_product_id": int,
      "promo_product_name": string,
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

| 필드 | 설명 |
|---|---|
| `slot_limit` | 이 상품에 동시 활성 가능한 최대 홍보 수. `promotion_products.slot_limit` 컬럼에서 읽음. 고정값으로 바뀌지 않음 |
| `remaining_slots` | 현재 활성 홍보 수를 빼서 동적 계산. DB 컬럼 없음. 누군가 신청할 때마다 줄고, 기간 만료로 홍보가 끝나면 다시 늘어남 |
| `is_available` | `remaining_slots > 0`이면 `true` |

**`slot_limit` vs `remaining_slots` 변화 예시 (팝업 상품, slot_limit = 5):**

| 상황 | slot_limit | remaining_slots |
|---|---|---|
| 초기 (신청 없음) | 5 | 5 |
| 유저 A 신청 후 | 5 | 4 |
| 유저 B, C, D, E 신청 후 | 5 | 0 → `is_available = false` |
| 유저 A의 홍보 만료 후 | 5 | 1 → `is_available = true` |

> `slot_limit`은 절대 바뀌지 않는다. `remaining_slots`만 실시간으로 바뀐다.

**카드 색상 기준:**
- 노란색(신청 가능): `is_available = true` AND 내 `current_points >= price`
- 빨간색(빡낌 부족): `is_available = true` AND 내 `current_points < price`
- 빨간색(슬롯 부족): `is_available = false`

> 두 조건이 겹칠 때(`is_available = false` AND `current_points < price`)는 슬롯 부족 우선 표시.

---

### GET /promotion-products/{promotion_product_id}

**언제 씀:** 홍보 신청 모달 열 때 단건 상세 조회

응답 구조는 목록의 `items` 단건과 동일.

---

### POST /promotions

**언제 씀:** 홍보 신청 모달에서 "신청 확인" 클릭 시

**Request**

```json
{ "promo_product_id": int, "service_id": int }
```

> `service_id`는 본인 서비스만 허용. 타인 서비스 신청 시 403.

**Error Response**

| HTTP 상태 | `detail` 값 | 의미 |
|---|---|---|
| 403 | `"forbidden_service"` | 본인 서비스가 아님 |
| 409 | `"slot_exhausted"` | 슬롯 소진 |
| 409 | `"already_promoted"` | 해당 서비스가 이미 활성 홍보 중 |
| 402 | `"insufficient_points"` | 빡낌 잔액 부족 |

> FastAPI `HTTPException(status_code=..., detail="...")` 형태로 반환. 프론트는 `detail` 값으로 메시지를 구분.

> **에러 체크 순서:** `forbidden_service` → `already_promoted` → `slot_exhausted` → `insufficient_points`. 복수 조건이 동시에 성립하면 위 순서에서 먼저 해당하는 에러만 반환.

**Response**

```json
{
  "promotion_id": int,
  "promo_product_name": string,
  "service_id": int,
  "start_at": datetime,
  "end_at": datetime,
  "status": string,
  "used_points": int,
  "current_points": int
}
```

| 필드 | 설명 |
|---|---|
| `start_at` / `end_at` | 신청 완료 모달에서 노출 기간 표시용 |
| `status` | 신청 직후 `"진행중"`. 만료 후에도 DB는 그대로이므로 조회 시 `end_at`으로 재계산 |
| `used_points` | 차감된 빡낌 (= 상품 가격). 모달 내 빡낌 요약 표시용 |
| `current_points` | 차감 후 잔액. 헤더 즉시 갱신에 사용 |

---

## 2. 빡낌 지급/차감 정책

| 시점 | 변동량 | 일일 제한 | 처리 위치 |
|---|---|---|---|
| 최초 가입 | +500 | - | User API |
| 피드백 approved | +200 | 3회 | Feedback API |
| 서비스 첫 피드백 | +300 | - | Feedback API (일반 +200 대신 지급, 중첩 없음) |
| 데일리 출석 | +100 | 1회 | POST /users/me/missions/attendance |
| 7 / 15 / 30일 연속 출석 달성 | +200 | - | POST /users/me/missions/attendance |
| 홍보 신청 | -상품 가격 | - | POST /promotions |

> **첫 피드백 기준:** 해당 서비스 전체에서 첫 번째로 달리는 피드백 작성자에게 +300 지급. 두 번째 피드백부터는 작성자에게 +200.

> **일일 3회 카운트 기준:** 일반 피드백(+200)과 첫 피드백(+300)을 통합 카운트. 하루에 3개 서비스에 첫 피드백을 달면 최대 900빡낌 획득 가능.

> **잔액 보호:** 차감 전 `current_points >= 차감액` 검증 필수. 0 미만 불가.

> **트랜잭션:** 모든 지급/차감은 `point_logs INSERT + users.current_points UPDATE` 단일 트랜잭션.

---

## 3. 출석 정책

| 항목 | 기준 |
|---|---|
| 날짜 기준 | KST (한국 시간 자정 기준) |
| 하루 제한 | 1회. 중복 요청 시 400 반환 |
| 연속 초기화 | 하루라도 빠지면 다음 출석 시 `streak_count = 1`부터 재시작 |
| 연속 보너스 | 7일 / 15일 / 30일 정확히 달성한 날 +200 추가 지급 (기본 +100 별도) |

> **streak 예시:** 3일 연속 출석 중 → 어제 결석 → 오늘 출석 → streak = 1, 보너스 없음.

---

## 4. 홍보 정책

### 상품 가격표

| 상품명 | 가격 | 슬롯 | duration_days |
|---|---|---|---|
| 홈 화면 크게 노출 | 5,000 | 5 | 1 |
| 상단 배너 | 4,000 | 5 | 1 |
| 추천 서비스(중간 크기의 서비스) | 3,000 | 5 | 1 |
| 서비스 카드(작은 크기의 서비스) | 1,500 | 20 | 1 |
| 팝업 | 1,000 | 5 | 1 |

> 1차 배포: 모든 상품 `duration_days = 1`

### 슬롯 관리

> **[Step 3]** — 홍보 신청(POST /promotions) 구현 범위

```
remaining_slots = slot_limit - COUNT(promotions
  WHERE promo_product_id = ?
  AND status = '진행중'
  AND end_at > NOW())
```

- `remaining_slots`는 DB 컬럼 없음 — 조회 시점에 동적 계산
- `end_at`은 POST /promotions 시점에 `신청 시각 + duration_days`로 계산해 DB에 저장. `NOW()`는 쿼리 실행 시각이므로 스케줄러 없이 만료가 자동 반영됨
- 동시에 여러 명이 신청하면 `SELECT FOR UPDATE`로 선착순 처리 (슬롯 초과 방지)
- 슬롯 소진 시 409 반환

### 만료 처리

> **[Step 4]** — 홍보 상태 관리 구현 범위

- 별도 스케줄러 없음. DB의 `status`는 변경하지 않음.
- 조회 시 `end_at < NOW()`이면 응답의 `status`를 `"종료됨"`으로 계산해서 반환

### 중복 신청 차단

> **[Step 4]** — 홍보 상태 관리 구현 범위

- **1차 차단 (프론트):** 모달 열릴 때 KEG 담당 `GET /users/me/promotions/active` 호출 → 응답의 `service_id` 목록으로 드롭다운에서 이미 홍보 중인 서비스 disabled + "홍보중" 라벨 표시
  > 이 API는 KEG(김은경) 담당 구현. 응답 구조는 KEG 계약서에 정의. PJB는 `service_id` 목록만 소비.
- **최후 방어 (백엔드):** 같은 서비스가 이미 활성 홍보 중이면 409 반환

### 홍보 노출 데이터

- 별도 소재 업로드 없음. `services` 테이블의 기존 필드 재사용:
  `title`, `summary`, `thumbnail_url`, `service_url`

---

## 5. promotion_products 초기 데이터

- **적재 방법:** Alembic migration에 포함 — 테이블 생성 직후 migration에서 INSERT
- 배포 시 자동 적재. 별도 seed 스크립트 없음.

| promo_product_name | price | slot_limit | duration_days | placement |
|---|---|---|---|---|
| 홈 화면 크게 노출 | 5000 | 5 | 1 | home_hero |
| 상단 배너 | 4000 | 5 | 1 | top_banner |
| 추천 서비스 | 3000 | 5 | 1 | recommended |
| 서비스 카드 | 1500 | 20 | 1 | service_card |
| 팝업 | 1000 | 5 | 1 | popup |

> `placement` 값은 프론트엔드 노출 위치 식별자. 확정 전 백엔드·프론트 협의 필요.

---

## 6. TABLE_DEF 변경 사항

| 테이블 | 항목 | 변경 내용 | 이유 | 담당 |
|---|---|---|---|---|
| `promotions` | `service_id` FK | `products(product_id)` → `services(service_id)` | 홍보 대상도 services로 통일 | PJB |
| `point_logs` | `current_points` 컬럼명·CHECK | `current_point` → `current_points`, CHECK `(current_points >= 0)` | 컬럼명 단수→복수 통일 및 CHECK 조건 반영 | PJB |
| `attendance` | `streak_count` | `INT NOT NULL DEFAULT 1` 추가 | 연속 출석일 추적에 필요 | PJB |
| `promotion_products` | `placement` | `VARCHAR NOT NULL` 추가 | 홍보 노출 위치 구분에 필요 | PJB |
| `promotion_products` | `slot_limit` | `INT NOT NULL CHECK (slot_limit > 0)` 추가 | 슬롯 수 관리에 필요 | PJB |
| `feedbacks` | `service_id` FK | `products(product_id)` → `services(service_id)` | 피드백 대상이 products가 아닌 services | # 김현진 |
| `community_comments` | `post_id` FK | `community_posts(c_post_id)` → `community_posts(post_id)` | PK 컬럼명 오류 수정 | # 담당자 확인 필요 |
| `user_follows` | UNIQUE | 단독 UNIQUE 2개 → 복합 UNIQUE `(follower_id, following_id)` | 동일 쌍 중복 팔로우를 DB 레벨에서 차단 | # 담당자 확인 필요 |

---

## 7. 미확정 사항 (구현 전 확인 필요)

### `services.status` 기준 — 조현정 확인 필요

`services.status` 허용값: `'대기중'`, `'활성'`, `'차단'`

홍보 신청 가능 조건을 어디까지로 볼지 확정이 필요하다.

| 옵션 | 조건 |
|---|---|
| A | `status = '활성'`인 서비스만 홍보 가능 |
| B | `status != '차단'`인 서비스는 홍보 가능 (`'대기중'` 포함) |

> PJB가 POST /promotions에서 서비스 status 체크 로직을 작성해야 하므로 구현 전 확정 필요.

---

## 8. 구현 규칙

> **[Step 2+ 공통]** — Step 1 계약 범위 외. Step 2부터 구현 전 단계에서 준수할 규칙

### 시각/날짜 처리 기준

시각과 날짜를 다루는 곳이 두 군데다. **용도에 따라 다른 함수를 써야 한다.**

**DB는 UTC로 저장, API 응답은 UTC ISO 8601, 프론트에서 KST로 변환해 표시한다.**

| 용도 | 함수 | 비고 |
|---|---|---|
| 출석 날짜 (`attended_date`) | `kst_today()` | KST 자정 기준 "오늘" 판단용. String `'YYYY-MM-DD'` 반환 |
| DB 저장 시각 (`end_at` 등) | `utc_now()` | PostgreSQL `NOW()`와 일관되도록 naive UTC 반환 |
| API 응답 datetime 직렬화 | `as_utc()` | FastAPI가 naive datetime을 직렬화할 때 UTC임을 명시 (`2026-06-19T01:00:00Z`) |

> **왜 UTC로 통일하나:** `server_default="now()"` 로 DB에 들어가는 시각은 EC2 서버 기준 UTC다. 변환 없이 그대로 반환하면 프론트가 UTC로 해석할 수 있다. 프론트는 `new Date("2026-06-19T01:00:00Z")`를 받아 KST로 표시한다.

> **`end_at`에 KST를 저장하면 안 되는 이유:** 슬롯 쿼리의 `end_at > NOW()`에서 PostgreSQL `NOW()`는 UTC이므로, KST 값을 넣으면 만료 판단이 9시간 늦어진다.

모든 시각/날짜는 `app/core/timezone.py`의 함수만 사용한다.

```python
# app/core/timezone.py
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))

def kst_now() -> datetime:
    return datetime.now(KST)

def kst_today() -> str:
    """출석 날짜 비교용 — KST 기준 오늘 날짜 문자열"""
    return kst_now().strftime("%Y-%m-%d")

def utc_now() -> datetime:
    """DB 저장용 naive UTC 시각 (PostgreSQL NOW()와 일관)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)

def as_utc(dt: datetime) -> datetime:
    """API 응답 직렬화용 — naive UTC datetime에 UTC timezone 부착"""
    return dt.replace(tzinfo=timezone.utc)
```
