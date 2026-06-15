# 조현정 작업 계획: 서비스 등록, 데이터 수집

## 목표

사용자가 조건을 충족한 뒤 자신의 서비스를 등록하고, 이후 추천/홍보/피드백/AI 고도화에 활용할 수 있는 서비스 데이터를 안정적으로 수집한다.

## 담당 기능 

- 서비스 등록 조건 확인
- 서비스 등록 폼
- 제목/내용 추천
- 카테고리 필수 선택
- URL 형식 및 접속 가능 여부 검증
- Google Web Risk API 기반 위험 URL 검사
- 서비스 목록/상세 조회용 기본 데이터 제공
- 서비스 상세 하단 동일 카테고리 랜덤 3개 추천
- 서비스 관련 데이터 수집 이벤트 정의

## 구현 범위

### 서비스 등록 조건

서비스 등록 전 아래 조건을 검사한다.

- 가입 후 24시간 이상 경과
- 다른 서비스에 승인된 피드백 1개 이상 작성

조건을 만족하지 못하면 등록을 막고, 미충족 사유를 화면에 반환한다.

### 서비스 등록

필수 입력값:

- 제목
- 설명
- 카테고리
- URL

저장 시 기본 상태는 `active` 또는 운영 검토 정책이 필요하면 `pending`으로 둔다. 1차 배포에서는 빠른 순환 검증이 목표이므로 위험 URL이 아니면 즉시 노출을 기본값으로 한다.

### 제목/내용 추천

1차 배포에서는 LLM 기반 추천을 우선하되, 실패 시 템플릿 문구를 반환한다.

추천 결과는 사용자가 수정할 수 있어야 하며, 최종 저장값은 사용자가 제출한 제목/내용이다.

### URL 검증

검증 순서:

1. URL 형식 검사
2. HTTP/HTTPS 프로토콜 검사
3. 접속 가능 여부 확인
4. Google Web Risk API 검사
5. 결과 저장

위험 URL이면 등록을 차단하고 `url_risk_status`에 실패 사유를 남긴다.

## 데이터 모델

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

### service_events

서비스 데이터 수집을 위해 이벤트 테이블을 둔다.

- id
- service_id
- user_id
- event_type
- metadata
- created_at

초기 이벤트 타입:

- `service_view`
- `service_register_start`
- `service_register_complete`
- `service_url_validation_failed`
- `similar_service_click`
- `recommendation_click`

## API 초안

- `GET /api/services`
- `GET /api/services/:id`
- `POST /api/services`
- `GET /api/services/register-eligibility`
- `POST /api/services/suggest-copy`
- `POST /api/services/validate-url`
- `GET /api/services/:id/similar`
- `POST /api/services/:id/events`

## 다른 담당자와 맞출 부분

- 김현진: 피드백 1개 이상 작성 여부 판단 기준
- 박재범: 홍보 구매 후 서비스 노출 우선순위 반영
- 박건일: 서비스 신고 대상 구조
- 김은경: 마이페이지의 내 서비스 목록 데이터

## 완료 기준

- 등록 조건을 만족한 사용자만 서비스를 등록할 수 있다.
- URL 검증 실패 시 등록이 차단된다.
- 등록된 서비스가 목록과 상세 화면에 노출된다.
- 서비스 상세 하단에 동일 카테고리 서비스가 최대 3개 노출된다.
- 핵심 조회/등록/추천 클릭 이벤트가 수집된다.
