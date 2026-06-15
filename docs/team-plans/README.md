# BuildBack 1차 배포 팀원별 계획

이 디렉터리는 `docs/phase1-plan.md`를 실제 구현 담당자별 작업 계획으로 나눈 문서 모음이다.

## 담당 범위 

| 담당자 | 범위 | 문서 |
| --- | --- | --- |
| 조현정 | 서비스 등록, 데이터 수집 | `cho-hyeonjeong-service-data.md` |
| 김현진 | 피드백, 소셜 로그인, 최초 로그인 관심분야 입력 | `kim-hyeonjin-auth-feedback-onboarding.md` |
| 박건일 | 커뮤니티 기능 전체 총괄, 신고 기능 | `park-geonil-community-report.md` |
| 김은경 | 마이페이지, 커뮤니티 댓글 기능 | `kim-eungyeong-mypage-comments.md` |
| 박재범 | 포인트 관련 기능 전체 | `park-jaebeom-points.md` |

## 공통 원칙

- 1차 배포는 빠른 검증이 목표이므로 기능은 작게 만들고, 데이터가 정확히 쌓이도록 한다.
- 포인트 증감은 반드시 박재범 담당 포인트 API 또는 공통 서비스를 통해 처리한다.
- 로그인 사용자 정보는 김현진 담당 인증 흐름의 `me` 응답을 기준으로 사용한다.
- 신고 대상은 서비스, 커뮤니티 글, 댓글까지 확장 가능하도록 `target_type`, `target_id` 구조로 맞춘다.
- 서비스, 피드백, 커뮤니티, 댓글은 향후 AI 분석에 사용할 수 있도록 작성 본문과 작성/수정 시각을 보존한다.
