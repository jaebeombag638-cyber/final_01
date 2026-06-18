# 통합 관리자 1차 배포 계획

## 문서 목적

이 문서는 5개 팀원 계획 문서의 step을 묶어 `develop` 브랜치에서 어떤 순서로 병합하고 검증할지 정리하는 통합 관리자 문서다.

통합 관리자 step은 독립 작업이 아니다. 각 통합 step은 조현정, 김현진, 박건일, 김은경, 박재범 문서의 step을 조합해 하나의 실행 가능한 통합 단위로 관리한다.

단, Step 0은 예외적으로 모든 기능 구현의 선행 조건인 backend DB 기반 설정 step이다. Step 0이 끝나기 전에는 팀원별 feature 브랜치에서 실제 API 저장/조회 연결을 완료 처리하지 않는다.

## 관리 대상 문서

| 담당자 | 문서 | 담당 범위 | 주요 브랜치 |
| --- | --- | --- | --- |
| 통합 관리자 | 이 문서 | 피그마 MCP 기반 프론트 기초 코드 통합, develop 병합 관리 | `frontend`, `develop` |
| 조현정 | `docs/team-plans/CHJ.md` | 서비스 등록 | `feature/service-registration` |
| 김현진 | `docs/team-plans/KHJ.md` | 피드백, 소셜 로그인, 관심분야 | `feature/login`, `feature/onboarding-interests`, `feature/feedback` |
| 박건일 | `docs/team-plans/PGI.md` | 커뮤니티, 신고 | `feature/posts`, `feature/reports` |
| 김은경 | `docs/team-plans/KEG.md` | 마이페이지, 댓글, 팔로우 | `feature/mypage`, `feature/comments`, `feature/follow` |
| 박재범 | `docs/team-plans/PJB.md` | 홍보, 포인트 | `feature/points`, `feature/promotions` |

## 통합 브랜치 규칙

- 피그마 MCP로 생성하는 프론트 기초 코드는 `frontend` 브랜치에서 먼저 구현한다.
- `frontend` 브랜치에는 피그마 화면 구조, 컴포넌트 배치, 기본 스타일, 목업 데이터 흐름을 담는다.
- 피그마 의도와 다르게 생성된 부분은 `frontend` 브랜치에서 1차 보정한 뒤 `develop`에 병합한다.
- 팀원은 각자 `feature/*` 브랜치에서 작업한다.
- 팀원별 `feature/*` 브랜치는 `frontend`가 병합된 `develop`에서 만든다.
- 팀원은 피그마 기반 프론트 코드를 새로 갈아엎지 않고, 담당 화면과 컴포넌트를 필요한 만큼 수정하면서 실제 기능을 붙인다.
- 통합 관리자는 필요한 `feature/*` 브랜치만 `develop`에 병합한다.
- 팀원은 `main`에 직접 병합하지 않는다.
- `develop`에서 통합 테스트를 통과한 상태만 `main`으로 병합한다.
- 통합 실패 시 원인 브랜치를 분리하고, 해당 통합 step을 완료 처리하지 않는다.

## 통합 Step 요약

| 통합 step | 포함 팀원 step | 통합 목표 | 완료 기준 |
| --- | --- | --- | --- |
| Step 0 | 공통 선행 작업 | DB 스키마와 연결 기반 확정 | PostgreSQL 연결, SQLAlchemy model, Alembic migration, 테스트 DB 적용 기준이 준비된다. |
| Step 1 | 전원 Step 1 | 기능 계약과 기본 골격 확정 | API, 테이블, 라우트, 브랜치 기준이 맞는다. |
| Step 2 | 전원 Step 2 | 핵심 조회 흐름 연결 | 서비스, 피드백, 게시글, 마이페이지, 포인트 조회가 동작한다. |
| Step 3 | 전원 Step 3 | 핵심 생성 흐름 연결 | 가입, 피드백, 서비스 등록, 게시글/댓글, 출석/홍보 신청이 동작한다. |
| Step 4 | 전원 Step 4 | 수정/삭제/상태 변경 연결 | 수정, 삭제, 블라인드, 홍보 상태 변경이 충돌 없이 동작한다. |
| Step 5 | 전원 Step 5 | 정책과 권한 검증 | 등록 조건, 피드백 제한, 신고 정책, 포인트/홍보 정책이 적용된다. |
| Step 6 | 전원 Step 6 | 담당 기능 간 1차 연결 | 핵심 루프가 기능 간 데이터로 이어진다. |
| Step 7 | 전원 Step 7 | 에러/빈 상태 통합 | 실패와 빈 상태가 화면별로 깨지지 않는다. |
| Step 8 | 전원 Step 8 | 운영 확인 데이터 연결 | 로그, 신고, 마이페이지, 포인트 이력 확인이 가능하다. |
| Step 9 | 전원 Step 9 | 전체 통합 시나리오 검증 | 핵심 사용자 루프가 `develop`에서 끝까지 동작한다. |
| Step 10 | 전원 Step 10 | 배포 전 점검 | 문서, 명세, 수동 체크리스트가 정리된다. |

## Step 0 : Backend DB 기반 설정

**포함되는 팀원 step**

- 공통 선행 작업이다.
- 팀원별 기능 Step 1보다 먼저 완료한다.
- DB 스키마 변경이 필요한 팀원별 작업은 이 step의 model, migration, 연결 규칙을 기준으로 진행한다.

**통합 목표**

`docs/TABLE_DEF.csv`를 기준으로 1차 배포에 필요한 PostgreSQL 스키마를 구현하고, FastAPI backend가 같은 DB 연결 방식과 migration 기준을 사용하게 한다.

**선행 조건**

- `docs/TECHSPEC.md`의 backend stack 기준을 따른다.
- `docs/TABLE_DEF.csv`의 테이블과 컬럼 정의를 최신 상태로 확인한다.
- `docs/API_SPEC.csv`에서 저장/조회에 필요한 식별자와 상태값을 확인한다.
- 로컬 개발 DB는 Docker PostgreSQL을 사용한다.
- 운영 DB는 AWS RDS PostgreSQL을 사용한다.

**구현 대상**

- backend 환경변수 `DATABASE_URL` 정의
- SQLAlchemy engine/session 구성
- FastAPI request 단위 DB session dependency 구성
- `docs/TABLE_DEF.csv` 기준 SQLAlchemy model 작성
- Alembic 초기 설정
- 1차 schema migration 생성
- 로컬 Docker PostgreSQL에 migration 적용
- 테스트 DB에 migration 적용하는 기준 정리
- seed가 필요한 최소 기준 데이터 정리: `categories`, `promotion_products`

**DB 스키마 정의 기준**

- `docs/TABLE_DEF.csv`가 1차 스키마의 기준 문서다.
- model 이름, table 이름, PK/FK, nullable 여부, 기본값, 상태값은 migration에 반영한다.
- CSV에 없는 컬럼이 구현에 필요하면 먼저 `docs/TABLE_DEF.csv`와 담당 팀원 문서의 보완 필요 항목에 남긴다.
- `users.user_id`, `services.service_id`, `feedbacks.feedback_id`, `community_posts.post_id`, `community_comments.comment_id`, `point_logs.point_log_id`, `promotions.promotion_id`, `report.report_id`는 기능 간 연결 식별자로 사용한다.
- 포인트, 홍보, 신고, 공개 상태처럼 상태값이 필요한 컬럼은 API 응답 상태값과 같은 용어로 맞춘다.

**DB 연결 기준**

- backend는 환경변수 `DATABASE_URL`로만 DB 접속 정보를 읽는다.
- 로컬 `.env`는 Docker PostgreSQL 연결 문자열을 사용한다.
- 운영 EC2 `.env`는 RDS PostgreSQL 연결 문자열을 사용한다.
- 테스트는 운영 DB와 분리된 테스트 DB 또는 테스트 schema를 사용한다.
- API handler는 직접 engine을 만들지 않고 공통 session dependency를 통해 DB에 접근한다.
- migration은 배포 시점에 EC2에서 일회성 Docker Compose 명령으로 실행한다.

**병합 대상 브랜치와 순서**

1. `develop`에서 backend DB 기반 작업 브랜치를 만든다.
2. DB 기반 작업 브랜치를 `develop`에 먼저 병합한다.
3. `frontend`를 `develop`에 병합한다.
4. 팀원별 `feature/*` 브랜치를 `develop`에서 생성한다.

**통합 테스트**

- 로컬 Docker PostgreSQL이 실행된다.
- backend가 `DATABASE_URL`로 DB에 연결된다.
- Alembic migration이 빈 DB에 끝까지 적용된다.
- migration 적용 후 주요 테이블이 생성된다.
- pytest에서 DB session dependency를 테스트 DB로 교체할 수 있다.
- `categories`, `promotion_products` 기준 데이터가 필요한 조회 API에서 사용 가능하다.

**통합 완료 조건**

- backend 공통 DB 연결 코드가 한 곳에만 존재한다.
- SQLAlchemy model과 Alembic migration이 `docs/TABLE_DEF.csv`와 불일치하지 않는다.
- 빈 PostgreSQL DB에서 migration만으로 1차 schema가 재현된다.
- 팀원별 Step 1에서 참조하는 주요 테이블이 모두 생성된다.
- DB 연결 실패, migration 실패, 테스트 DB 미분리 상태가 남아 있지 않다.

**실패 시 되돌림 기준**

- migration이 빈 DB에 적용되지 않으면 Step 1로 넘어가지 않는다.
- model과 migration이 다르면 migration을 우선 수정하고 기능 브랜치 병합을 중단한다.
- 운영 RDS 연결 정보가 코드에 직접 들어가면 병합하지 않는다.
- 테스트가 운영 DB에 연결될 수 있으면 병합하지 않는다.

## Step 1 : 기능 계약과 기본 골격 통합

**포함되는 팀원 step**

- 김현진 Step 1 : 기능 계약 확인
- 조현정 Step 1 : 기능 계약 확인
- 박재범 Step 1 : 기능 계약 확인
- 박건일 Step 1 : 기능 계약 확인
- 김은경 Step 1 : 기능 계약 확인

**통합 목표**

피그마 MCP 기반 프론트 기초 코드를 `frontend` 브랜치에서 먼저 만들고, 로그인 사용자, 서비스, 피드백, 포인트, 커뮤니티, 신고, 마이페이지가 같은 API와 테이블 기준을 보도록 계약을 맞춘다.

**선행 조건**

- Step 0에서 DB 스키마와 DB 연결 기반이 완료되어야 한다.
- 피그마 화면이 최신 상태로 준비되어 있어야 한다.
- `docs/API_SPEC.csv`와 `docs/TABLE_DEF.csv`를 최신 상태로 확인한다.
- 각 팀원 문서의 주요 계약 섹션이 비어 있지 않아야 한다.
- `frontend` 브랜치가 생성되어 있어야 한다.
- 각 담당자의 기본 `feature/*` 브랜치는 `frontend` 병합 이후 생성한다.

**병합 대상 브랜치와 순서**

1. `frontend`
2. `feature/login`
3. `feature/service-registration`
4. `feature/points`
5. `feature/posts`
6. `feature/mypage`

**통합 테스트**

- `frontend` 브랜치에서 생성된 피그마 기반 화면이 주요 라우트에 연결되어 있는지 확인한다.
- 피그마와 다르게 보이는 구조적 차이가 있으면 `frontend`에서 1차 보정한다.
- 로그인 모달 또는 목업 로그인 진입이 가능하다.
- 서비스 페이지, 커뮤니티 페이지, 마이페이지, 홍보 상품 영역에 기본 라우트로 접근한다.
- 각 화면이 목업 또는 기본 응답으로 렌더링된다.

**통합 완료 조건**

- 공통 사용자 식별값은 `user_id`로 맞춘다.
- 서비스 식별값은 `service_id`로 맞춘다.
- 게시글, 댓글, 신고, 포인트 로그의 식별값이 명세와 충돌하지 않는다.
- API_SPEC에 아직 없는 API는 보완 필요 항목으로 표시되어 있다.
- 팀원별 `feature/*` 작업은 `frontend`가 병합된 `develop` 기준에서 시작할 수 있다.

**실패 시 되돌림 기준**

- 피그마 기초 화면이 주요 라우트에서 깨지면 `frontend`를 `develop`에 병합하지 않는다.
- 공통 식별자나 라우트가 충돌하면 병합을 중단하고 원인 브랜치를 `develop`에서 제외한다.
- API 명세가 서로 다르면 구현을 우선하지 않고 명세를 먼저 수정한다.

## Step 2 : 핵심 조회 흐름 통합

**포함되는 팀원 step**

- 조현정 Step 2 : 서비스 목록/상세 조회
- 김현진 Step 2 : 피드백과 관심 카테고리 조회
- 박건일 Step 2 : 게시글과 신고 목록 조회
- 김은경 Step 2 : 마이페이지, 댓글, 팔로우 조회
- 박재범 Step 2 : 포인트, 출석, 홍보 상품 조회

**통합 목표**

사용자가 가입 전후에 탐색할 수 있는 주요 조회 화면을 `develop`에서 연결한다.

**선행 조건**

- Step 1에서 라우트와 기본 응답 구조가 확정되어야 한다.
- 조회 API의 인증 필요 여부가 정리되어야 한다.

**병합 대상 브랜치와 순서**

1. `feature/login`
2. `feature/service-registration`
3. `feature/feedback`
4. `feature/posts`
5. `feature/comments`
6. `feature/mypage`
7. `feature/points`
8. `feature/promotions`

**통합 테스트**

- `GET /services`와 `GET /services/{service_id}`로 서비스 목록/상세를 조회한다.
- 서비스 상세에서 피드백 목록을 조회한다.
- 커뮤니티 게시글 목록/상세를 조회한다.
- 마이페이지에서 내 정보, 내 서비스, 내 피드백, 포인트 요약을 조회한다.
- 홍보 상품 목록과 포인트 잔액을 조회한다.

**통합 완료 조건**

- 각 조회 화면이 빈 상태와 데이터 있는 상태를 모두 표시한다.
- 헤더 잔액과 마이페이지 잔액이 같은 값을 바라본다.
- 서비스 상세, 게시글 상세, 마이페이지가 서로 필요한 데이터 식별자를 공유한다.

**실패 시 되돌림 기준**

- 조회 API 응답 필드가 화면 요구와 맞지 않으면 해당 브랜치를 제외하고 API_SPEC를 먼저 수정한다.
- 인증이 필요한 API가 비로그인 화면을 깨뜨리면 인증 처리 기준을 먼저 정리한다.

## Step 3 : 핵심 생성 흐름 통합

**포함되는 팀원 step**

- 김현진 Step 3 : 로그인, 온보딩, 피드백 작성
- 조현정 Step 3 : 서비스 등록
- 박건일 Step 3 : 게시글 작성, 신고 접수
- 김은경 Step 3 : 댓글 작성, 팔로우
- 박재범 Step 3 : 출석 체크, 홍보 신청

**통합 목표**

사용자가 실제로 가입하고, 콘텐츠를 만들고, 피드백과 포인트를 발생시키는 생성 흐름을 연결한다.

**선행 조건**

- Step 2의 조회 흐름이 동작해야 한다.
- 신규 사용자 세션과 기존 사용자 세션 흐름이 구분되어야 한다.

**병합 대상 브랜치와 순서**

1. `feature/login`
2. `feature/onboarding-interests`
3. `feature/feedback`
4. `feature/service-registration`
5. `feature/posts`
6. `feature/comments`
7. `feature/follow`
8. `feature/points`
9. `feature/promotions`

**통합 테스트**

- 신규 사용자가 구글 로그인 후 닉네임과 관심 카테고리를 설정한다.
- 사용자가 타인 서비스에 피드백을 작성한다.
- 등록 조건을 만족한 사용자가 서비스를 등록한다.
- 사용자가 커뮤니티 게시글과 댓글을 작성한다.
- 사용자가 출석 체크를 하고 홍보 신청을 진행한다.

**통합 완료 조건**

- 신규 가입부터 서비스 등록까지 핵심 루프가 끊기지 않는다.
- 피드백 작성 후 포인트 지급 이벤트가 발생한다.
- 서비스 등록 후 마이페이지와 홍보 신청 대상에 반영된다.
- 게시글과 댓글 생성 후 신고 대상이 될 수 있다.

**실패 시 되돌림 기준**

- 생성 API 중 하나가 공통 세션을 깨뜨리면 해당 브랜치를 제외한다.
- 포인트 지급이 중복되거나 누락되면 홍보 신청 통합을 진행하지 않는다.

## Step 4 : 수정, 삭제, 상태 변경 통합

**포함되는 팀원 step**

- 김현진 Step 4 : 피드백 수정/삭제
- 조현정 Step 4 : 서비스 수정/삭제/상태 변경
- 박건일 Step 4 : 게시글 수정/삭제, 신고 처리
- 김은경 Step 4 : 댓글 수정/삭제, 언팔로우
- 박재범 Step 4 : 홍보 진행 상태와 만료 처리

**통합 목표**

작성자 권한, 삭제 정책, 블라인드, 홍보 상태 변경이 서로 충돌하지 않도록 연결한다.

**선행 조건**

- Step 3에서 생성된 데이터가 있어야 한다.
- 각 콘텐츠의 작성자 식별 기준이 `user_id`로 통일되어야 한다.

**병합 대상 브랜치와 순서**

1. `feature/login`
2. `feature/service-registration`
3. `feature/feedback`
4. `feature/posts`
5. `feature/comments`
6. `feature/reports`
7. `feature/promotions`

**통합 테스트**

- 작성자가 본인 서비스, 피드백, 게시글, 댓글을 수정한다.
- 타인이 수정/삭제를 시도하면 차단된다.
- 신고 승인 후 서비스/게시글/댓글이 블라인드된다.
- 홍보 중인 서비스가 차단되면 홍보 노출이 중단된다.

**통합 완료 조건**

- 권한 실패와 정책 실패가 구분된다.
- 블라인드 상태가 목록, 상세, 마이페이지, 홍보 노출에 반영된다.
- 홍보 만료 상태가 활성 홍보 목록에서 제외된다.

**실패 시 되돌림 기준**

- 블라인드 처리 후 다른 화면에서 여전히 노출되면 해당 대상 기능 브랜치를 제외한다.
- 삭제가 실제 삭제인지 상태 변경인지 불명확하면 API 정책 확정 전 병합하지 않는다.

## Step 5 : 정책, 제한, 권한 통합

**포함되는 팀원 step**

- 김현진 Step 5 : 피드백 작성 제한과 품질 검사
- 조현정 Step 5 : 서비스 등록 조건과 URL 검증
- 박건일 Step 5 : 커뮤니티 권한과 욕설 필터링
- 김은경 Step 5 : 댓글/팔로우 권한과 제한
- 박재범 Step 5 : 포인트/홍보 정책 검증

**통합 목표**

1차 배포의 핵심 정책이 실제 사용자 행동을 올바르게 막거나 허용하는지 검증한다.

**선행 조건**

- 생성/수정 흐름이 동작해야 한다.
- 테스트 계정은 신규, 24시간 경과, 포인트 보유, 포인트 부족, 관리자 계정으로 나눈다.

**병합 대상 브랜치와 순서**

1. `feature/login`
2. `feature/feedback`
3. `feature/service-registration`
4. `feature/points`
5. `feature/promotions`
6. `feature/posts`
7. `feature/comments`
8. `feature/follow`
9. `feature/reports`

**통합 테스트**

- 가입 24시간 미만 사용자의 서비스 등록을 차단한다.
- 피드백 1건 미작성 사용자의 서비스 등록을 차단한다.
- 본인 서비스 피드백 작성을 차단한다.
- 피드백 일일 4번째 작성을 차단한다.
- 욕설 포함 게시글 작성을 차단한다.
- 자기 자신 팔로우와 중복 팔로우를 차단한다.
- 잔액 부족, 슬롯 부족, 중복 홍보 신청을 차단한다.

**통합 완료 조건**

- 차단 사유가 사용자에게 구체적으로 표시된다.
- 정책 차단이 포인트, 마이페이지, 홍보 상태를 오염시키지 않는다.
- 승인된 피드백에만 보상이 지급된다.

**실패 시 되돌림 기준**

- 정책 실패가 데이터 저장 이후에 발생하면 해당 생성 브랜치를 제외한다.
- 포인트가 잘못 지급되면 `feature/points`와 호출 브랜치를 함께 재검토한다.

## Step 6 : 담당 기능 간 1차 연결 통합

**포함되는 팀원 step**

- 김현진 Step 6 : 피드백 성공 이벤트와 포인트/서비스 등록 연결
- 조현정 Step 6 : 서비스와 피드백/홍보/신고/마이페이지 연결
- 박건일 Step 6 : 신고 대상 공통 연결
- 김은경 Step 6 : 마이페이지 데이터 연결
- 박재범 Step 6 : 포인트 지급과 홍보 노출 연결

**통합 목표**

BuildBack의 핵심 순환 구조가 기능 간 데이터로 이어지게 한다.

**선행 조건**

- Step 5의 정책 검증을 통과해야 한다.
- 각 기능은 독립 생성/조회가 가능해야 한다.

**병합 대상 브랜치와 순서**

1. `feature/login`
2. `feature/feedback`
3. `feature/points`
4. `feature/service-registration`
5. `feature/promotions`
6. `feature/posts`
7. `feature/comments`
8. `feature/reports`
9. `feature/mypage`

**통합 테스트**

- 피드백 승인 후 200빡낌 또는 첫 피드백 300빡낌이 지급된다.
- 가입 24시간 경과와 피드백 1건 조건이 충족되면 서비스 등록 모달이 바뀐다.
- 등록된 서비스가 홍보 신청 드롭다운에 나온다.
- 홍보 신청 후 서비스 목록 노출에 반영된다.
- 서비스, 피드백, 게시글, 댓글 신고가 같은 관리자 목록에 들어온다.
- 마이페이지에 서비스, 피드백, 댓글, 홍보, 포인트가 반영된다.

**통합 완료 조건**

- 핵심 루프 `로그인 -> 피드백 -> 포인트 -> 서비스 등록 -> 홍보 -> 피드백 수집`이 동작한다.
- 기능 간 연결 데이터가 중복 생성되지 않는다.
- 마이페이지는 각 기능의 최신 상태를 보여준다.

**실패 시 되돌림 기준**

- 연결 이벤트가 중복 처리되면 이벤트 호출 쪽 브랜치를 제외한다.
- 마이페이지 데이터가 맞지 않으면 원천 API와 마이페이지 브랜치를 함께 확인한다.

## Step 7 : 에러, 빈 상태, 예외 케이스 통합

**포함되는 팀원 step**

- 전원 Step 7

**통합 목표**

비로그인, 빈 목록, 권한 없음, 정책 차단, 외부 API 실패 같은 예외 상황에서 전체 화면이 깨지지 않게 한다.

**선행 조건**

- Step 6의 기능 연결이 동작해야 한다.

**병합 대상 브랜치와 순서**

1. `feature/login`
2. `feature/service-registration`
3. `feature/feedback`
4. `feature/posts`
5. `feature/comments`
6. `feature/follow`
7. `feature/points`
8. `feature/promotions`
9. `feature/reports`
10. `feature/mypage`

**통합 테스트**

- 비로그인 사용자가 글쓰기/댓글/피드백/홍보를 시도한다.
- 서비스 없는 카테고리, 댓글 없는 게시글, 활동 없는 마이페이지를 확인한다.
- Web Risk 실패, LLM 품질 실패, 잔액 부족, 슬롯 부족을 발생시킨다.
- 신고 사유 누락과 기타 사유 미입력을 확인한다.

**통합 완료 조건**

- 모든 빈 상태가 영역별로 표시된다.
- 실패 케이스가 공통 오류로 뭉개지지 않는다.
- 실패 후 데이터가 불완전하게 저장되지 않는다.

**실패 시 되돌림 기준**

- 예외 처리 실패가 화면 전체 장애를 만들면 해당 화면 브랜치를 제외한다.
- 외부 API 실패가 등록/작성 데이터를 저장하면 해당 기능을 완료 처리하지 않는다.

## Step 8 : 관리자와 운영 확인 데이터 통합

**포함되는 팀원 step**

- 조현정 Step 8 : 서비스 진입 로그
- 김현진 Step 8 : 피드백 품질 결과와 제한 판단 데이터
- 박건일 Step 8 : 관리자 신고 처리
- 김은경 Step 8 : 사용자 활동 정보
- 박재범 Step 8 : 포인트 로그와 홍보 내역

**통합 목표**

운영자가 신고, 포인트, 서비스, 사용자 활동을 확인할 수 있는 최소 데이터를 연결한다.

**선행 조건**

- Step 6과 Step 7에서 정상/실패 흐름이 모두 저장 기준을 갖춰야 한다.

**병합 대상 브랜치와 순서**

1. `feature/reports`
2. `feature/posts`
3. `feature/comments`
4. `feature/service-registration`
5. `feature/feedback`
6. `feature/points`
7. `feature/promotions`
8. `feature/mypage`

**통합 테스트**

- 서비스 상세 진입 로그가 저장된다.
- 피드백 품질 결과와 글자수가 저장된다.
- 포인트 지급/차감 로그가 저장된다.
- 신고 목록에서 서비스, 피드백, 게시글, 댓글 신고를 확인한다.
- 신고 승인 후 대상이 블라인드된다.

**통합 완료 조건**

- 관리자 또는 운영자가 신고 대상과 포인트 이력을 확인할 수 있다.
- 포인트 로그는 수정/삭제되지 않는다.
- 서비스 진입 로그는 홍보 유입과 일반 유입을 구분한다.

**실패 시 되돌림 기준**

- 운영 로그가 누락되면 관련 기능은 배포 완료 조건에서 제외한다.
- 신고 승인 후 대상 상태가 바뀌지 않으면 신고 브랜치와 대상 기능 브랜치를 함께 제외한다.

## Step 9 : 전체 통합 테스트

**포함되는 팀원 step**

- 전원 Step 9

**통합 목표**

1차 배포 핵심 루프를 실제 사용자 시나리오로 끝까지 검증한다.

**선행 조건**

- Step 8까지의 통합 완료 조건을 만족해야 한다.
- 테스트 계정, 관리자 계정, 테스트 서비스, 테스트 홍보 상품이 준비되어야 한다.

**병합 대상 브랜치와 순서**

1. `feature/login`
2. `feature/onboarding-interests`
3. `feature/service-registration`
4. `feature/feedback`
5. `feature/points`
6. `feature/promotions`
7. `feature/posts`
8. `feature/comments`
9. `feature/follow`
10. `feature/reports`
11. `feature/mypage`

**통합 테스트**

1. 신규 사용자가 구글 로그인한다.
2. 닉네임과 관심 카테고리를 설정한다.
3. 서비스 목록에서 타인 서비스를 탐색한다.
4. 피드백을 작성하고 품질 검사를 통과한다.
5. 피드백 보상과 첫 피드백 보상을 확인한다.
6. 가입 24시간 경과 조건과 피드백 1건 조건을 만족한 뒤 서비스를 등록한다.
7. 등록 서비스를 홍보 상품으로 신청한다.
8. 홍보 노출이 서비스 목록 또는 노출 영역에 반영된다.
9. 커뮤니티 게시글과 댓글을 작성한다.
10. 서비스, 피드백, 게시글, 댓글을 신고한다.
11. 관리자가 신고를 승인하고 블라인드 처리를 확인한다.
12. 마이페이지에서 서비스, 피드백, 댓글, 팔로우, 포인트, 홍보 내역을 확인한다.

**통합 완료 조건**

- 1차 배포 완료 기준의 모든 항목이 통과된다.
- 핵심 지표 측정에 필요한 데이터가 저장된다.
- `develop`에서 치명적인 화면 오류 없이 핵심 루프가 완료된다.

**실패 시 되돌림 기준**

- 핵심 루프를 끊는 브랜치는 `develop`에서 제외하고 해당 통합 step을 미완료로 남긴다.
- 포인트나 신고처럼 데이터 정합성에 영향을 주는 실패는 임시 우회하지 않는다.

## Step 10 : 배포 전 점검과 main 병합

**포함되는 팀원 step**

- 전원 Step 10

**통합 목표**

문서, 명세, 체크리스트, 브랜치 상태를 정리하고 `main` 병합 가능 여부를 판단한다.

**선행 조건**

- Step 9 전체 통합 테스트가 통과되어야 한다.
- `develop`에 병합된 모든 브랜치의 변경 범위가 확인되어야 한다.

**병합 대상 브랜치와 순서**

1. `develop` 상태 고정
2. 최종 문서 변경 반영
3. 배포 전 체크리스트 실행
4. `develop`에서 `main`으로 병합

**통합 테스트**

- `docs/API_SPEC.csv`에 실제 사용 API가 반영되어 있는지 확인한다.
- `docs/TABLE_DEF.csv`와 구현 필드 불일치가 없는지 확인한다.
- 팀원별 문서의 확인 방법을 따라 수동 QA를 1회 실행한다.
- 관리자 신고 처리와 포인트 이력 확인을 재검증한다.

**통합 완료 조건**

- `develop`의 핵심 시나리오가 통과된다.
- 배포 전 체크리스트가 완료된다.
- 배포 제외 기능이 있다면 문서에 명시된다.
- `main` 병합 후 1차 배포 후보 상태가 된다.

**실패 시 되돌림 기준**

- `main` 병합 전 실패가 발견되면 `develop`에 머무르고 원인 브랜치를 분리한다.
- `main` 병합 후 실패가 발견되면 배포를 중단하고 `develop`에서 수정 후 다시 병합한다.
