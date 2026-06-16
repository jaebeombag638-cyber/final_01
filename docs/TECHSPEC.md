# TECHSPEC

> BuildBack 1차 배포 구현 기준 기술 명세. 현재 프론트엔드 샘플 코드가 Next.js 구조여도, 실제 1차 구현은 React + Vite 기준으로 진행한다.

## 기본 스택

| 구분 | Techspec |
|---|---|
| Frontend 언어 | TypeScript |
| Frontend 런타임 | Node.js 20+ |
| Frontend 라이브러리 | React |
| Frontend 빌드 도구 | Vite |
| Frontend 라우팅 | React Router |
| UI 스타일링 | Tailwind CSS |
| Frontend 화면 QA 도구 | Playwright |
| Frontend 실행 명령 | npm run dev |
| Backend 언어 | Python 3.10 |
| Backend 프레임워크 | FastAPI |
| 데이터 검증 | Pydantic |
| ORM | SQLAlchemy |
| DB 마이그레이션 | Alembic |
| Backend 테스트 도구 | pytest |
| DB | PostgreSQL |

## 인증/외부 API

| 구분 | Techspec |
|---|---|
| 소셜 로그인 | Google OAuth |
| 인증 유지 방식 | HTTP-only Cookie Session |
| LLM | OpenAI API |
| URL 위험 검사 | Google Web Risk API |

## 로컬 개발

| 구분 | Techspec |
|---|---|
| 로컬 DB | Docker PostgreSQL |
| Backend 실행 | uvicorn |
| Frontend 실행 | Vite dev server |
| 환경변수 | .env.local, .env |

## AWS 배포

1차 배포는 AWS의 가장 기본적인 구성으로 시작한다. 운영 자동화보다 배포 성공과 유지보수 단순성을 우선한다.

| 구분 | Techspec |
|---|---|
| Frontend 배포 | AWS S3 + CloudFront |
| Backend 컨테이너 런타임 | Docker |
| Backend 서버 | AWS EC2 |
| Backend 실행 방식 | Docker Compose |
| Backend 외부 노출 | Nginx Reverse Proxy on EC2 |
| 운영 DB | AWS RDS PostgreSQL |
| 비밀값 관리 | EC2 `.env` 파일 |
| DNS | 1차 배포에서는 선택사항 |
| HTTPS 인증서 | 1차 배포에서는 선택사항 |
| 로그 | EC2 Docker logs |
| 모니터링 | EC2 기본 상태 확인 |

## Docker 배포 단위

### Backend

- FastAPI 애플리케이션을 Docker 이미지로 빌드한다.
- 1차 배포에서는 EC2에서 직접 이미지를 빌드한다.
- EC2에서는 Docker Compose로 backend 컨테이너를 실행한다.
- 외부 요청은 EC2의 Nginx reverse proxy를 통해 backend 컨테이너로 전달한다.
- DB 마이그레이션은 배포 시점에 EC2에서 일회성 Docker Compose 명령으로 실행한다.
- 환경변수와 API key는 EC2의 `.env` 파일로 주입한다.

### Frontend

- Vite 빌드 결과물인 `dist/`는 S3에 업로드하고 CloudFront로 배포한다.
- API 서버 주소는 환경별 설정으로 주입한다.

### DB

- PostgreSQL은 컨테이너로 직접 띄우지 않고 RDS를 사용한다.
- Backend EC2 인스턴스는 RDS 보안 그룹을 통해 PostgreSQL에 접근한다.

## 아직 결정해야 할 사항

- AWS 인프라 구성 도구: 1차 배포는 콘솔 수동 구성
- CI/CD 도구: 1차 배포 이후 도입 여부 결정
- 환경 분리: dev, staging, prod를 처음부터 나눌지 여부
- 도메인 구조: `buildback.kr`, `api.buildback.kr`처럼 분리할지 여부
- 세션 저장소: DB 기반 세션, Redis 기반 세션, 서명 쿠키 중 선택
- Redis 사용 여부: 세션, rate limit, 캐시가 필요하면 ElastiCache Redis 도입

## 1차 이후 고도화 후보

- Route 53 도메인 연결
- ACM 인증서 기반 HTTPS
- ECR 이미지 레지스트리
- GitHub Actions CI/CD
- Secrets Manager 또는 SSM Parameter Store
- CloudWatch Logs/Alarm
