# 김은경 작업 계획: 마이페이지, 커뮤니티 댓글, 팔로우/팔로잉 기능

## 목표

사용자가 자신의 활동, 포인트, 서비스, 피드백을 확인할 수 있는 마이페이지를 만들고, 커뮤니티 게시글에 댓글로 대화할 수 있는 기본 기능을 제공한다.

## 담당 기능

- 마이페이지
- 내 프로필 정보 조회
- 내 서비스 목록
- 내 피드백 목록
- 내 커뮤니티 글 목록
- 내 댓글 목록
- 내 포인트 요약 조회
- 커뮤니티 댓글 작성/수정/삭제
- 댓글 신고 연동
- 팔로우/팔로잉 기능

## 구현 범위

### 마이페이지

마이페이지에서 보여줄 정보:

- 닉네임
- 프로필 이미지
- 가입일
- 보유 빡낌
- 관심분야
- 내가 등록한 서비스
- 내가 작성한 피드백
- 내가 작성한 커뮤니티 글
- 내가 작성한 댓글
- 최근 포인트 이력
- 팔로우/팔로잉 수
- 팔로우/팔로잉 목록
- 서비스 별 피드백 수 변화 그래프

포인트 잔액과 이력은 박재범 담당 API를 사용한다.

### 댓글 기능

커뮤니티 게시글 상세에서 댓글을 작성할 수 있다.

1차 배포 댓글 정책:

- 로그인 사용자만 작성 가능
- 게시글이 `active` 상태일 때만 작성 가능
- 댓글 작성/수정 시 키워드 필터링 적용
- 댓글 삭제는 실제 삭제가 아니라 `deleted` 상태로 변경
- 신고 처리 시 `hidden` 상태로 변경 가능
- 대댓글은 1차 배포 범위에서 제외

### 댓글 표시

댓글 목록은 작성순으로 노출한다.

상태별 표시:

- `active`: 정상 노출
- `hidden`: "운영 정책에 따라 숨김 처리된 댓글입니다." 표시
- `deleted`: "삭제된 댓글입니다." 표시

## 데이터 모델

### community_comments

- id
- post_id
- author_user_id
- content
- status
- created_at
- updated_at
- deleted_at

### mypage summary 응답

마이페이지는 여러 담당 영역의 데이터를 모아 보여주는 화면이므로, API 응답을 요약형으로 둔다.

- user
- interests
- point_summary
- services
- feedbacks
- community_posts
- community_comments

## API 초안 

- `GET /api/me`
- `GET /api/me/summary`
- `GET /api/me/services`
- `GET /api/me/feedbacks`
- `GET /api/me/community-posts`
- `GET /api/me/community-comments`
- `GET /api/community/posts/:id/comments`
- `POST /api/community/posts/:id/comments`
- `PATCH /api/community/comments/:id`
- `DELETE /api/community/comments/:id`
- `POST /api/community/comments/:id/report`

## 다른 담당자와 맞출 부분

- 박재범: 포인트 잔액, 최근 포인트 이력 API
- 조현정: 내 서비스 목록 응답 필드
- 김현진: 내 피드백 목록 응답 필드와 로그인 사용자 정보
- 박건일: 커뮤니티 게시글 상세, 댓글 키워드 필터링, 댓글 신고 처리

## 완료 기준

- 로그인 사용자가 마이페이지에서 자신의 핵심 활동을 확인할 수 있다.
- 사용자가 커뮤니티 글에 댓글을 작성할 수 있다.
- 댓글 수정/삭제가 동작한다.
- 댓글에 키워드 필터링이 적용된다.
- 댓글 신고가 박건일 담당 신고 시스템으로 접수된다.
- 마이페이지의 포인트 정보가 박재범 담당 원장/잔액과 일치한다.
