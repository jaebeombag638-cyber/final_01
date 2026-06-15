# 박건일 작업 계획: 커뮤니티 기능 전체 총괄, 신고 기능

## 목표

빌더들이 자유롭게 경험과 요청을 남길 수 있는 커뮤니티 게시판을 만들고, 서비스/게시글/댓글 신고를 수동 운영 가능한 형태로 처리한다.

## 담당 기능

- 커뮤니티 게시판 구조 설계
- 게시글 목록/상세/작성/수정/삭제
- 게시글 키워드 필터링
- 커뮤니티 기능 전체 정책 정리
- 서비스 신고
- 커뮤니티 글 신고
- 댓글 신고 구조 협의
- 관리자 신고 처리 화면 또는 API

## 구현 범위

### 게시판

1차 배포 게시판:

- 자유게시판
- 팀 구하기
- 조빡낌한테건의하기

게시판 타입은 코드값으로 관리한다.

- `free`
- `team`
- `suggestion`

### 게시글

게시글 필드:

- 제목
- 내용
- 게시판 타입
- 작성자
- 상태

상태값:

- `active`
- `hidden`
- `deleted`

삭제는 실제 삭제보다 상태 변경을 기본으로 한다. 향후 신고/운영 이력을 확인해야 하기 때문이다.

### 키워드 필터링

글 작성 및 수정 시 키워드 필터링을 실행한다.

차단 대상:

- 욕설
- 혐오 표현
- 불법 홍보
- 스팸 키워드
- 개인정보 유도 문구

필터링 결과는 사용자에게 수정 가능한 안내 문구로 반환한다.

### 신고 기능

신고 대상: 

- 서비스
- 커뮤니티 글
- 커뮤니티 댓글

신고 사유:

- 스팸/홍보 도배
- 부적절한 콘텐츠
- 사기 또는 위험한 URL
- 개인정보 침해
- 기타

신고 처리는 1차 배포에서 관리자 수동 처리로 한다.

관리자 처리 액션:

- 신고 확인
- 대상 숨김
- 대상 유지
- 사용자 제재 필요 표시
- 처리 메모 작성

## 데이터 모델

### community_posts

- id
- board_type
- author_user_id
- title
- content
- status
- created_at
- updated_at

### keyword_filter_logs

- id
- target_type
- target_id
- user_id
- matched_keyword
- action
- created_at

### reports

- id
- reporter_user_id
- target_type
- target_id
- reason
- detail
- status
- admin_memo
- created_at
- resolved_at

`target_type` 후보:

- `service`
- `community_post`
- `community_comment`

## API 초안

- `GET /api/community/posts`
- `GET /api/community/posts/:id`
- `POST /api/community/posts`
- `PATCH /api/community/posts/:id`
- `DELETE /api/community/posts/:id`
- `POST /api/reports`
- `GET /api/admin/reports`
- `PATCH /api/admin/reports/:id`

## 다른 담당자와 맞출 부분

- 김은경: 댓글 데이터 모델, 댓글 신고 버튼, 댓글 숨김 정책
- 조현정: 서비스 신고 대상 구조와 서비스 숨김 처리
- 김현진: 로그인 사용자와 정지 사용자 권한 처리
- 박재범: 신고로 인한 포인트 회수는 1차 배포 자동 처리에서 제외하고 수동 운영으로 둘지 결정

## 완료 기준

- 사용자가 3개 게시판에 글을 작성할 수 있다.
- 게시글 작성/수정 시 키워드 필터링이 동작한다.
- 서비스, 커뮤니티 글, 댓글 신고가 같은 신고 테이블로 접수된다.
- 운영자가 신고 목록을 확인하고 상태를 변경할 수 있다.
- 신고 처리 결과에 따라 게시글 또는 신고 대상이 숨김 처리될 수 있다.
