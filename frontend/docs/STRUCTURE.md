# Frontend Structure

현재 프론트엔드는 Vite, React, TypeScript, Tailwind CSS 기반 프로젝트다.
아래 구조는 소스 코드와 프로젝트 설정 파일 기준이며, 로컬 생성물인 `node_modules`, `dist`는 제외했다.

```text
frontend/
├── .gitignore               # 프론트엔드에서 Git에 올리지 않을 파일 규칙
├── README.md                # 프론트엔드 실행 방법과 협업 규칙
├── eslint.config.js         # ESLint 설정 파일
├── index.html               # Vite가 사용하는 HTML 진입 파일
├── package.json             # npm 스크립트와 프론트엔드 의존성 선언
├── package-lock.json        # npm 의존성 잠금 파일
├── postcss.config.js        # PostCSS 설정 파일
├── tailwind.config.js       # Tailwind CSS 설정 파일
├── tsconfig.json            # TypeScript 공통 설정 진입 파일
├── tsconfig.app.json        # 앱 코드용 TypeScript 설정
├── tsconfig.node.json       # Node 환경 설정 파일용 TypeScript 설정
├── vite.config.ts           # Vite 개발 서버와 빌드 설정
├── docs/
│   └── structure.md         # 프론트엔드 디렉토리 구조 설명 문서
├── public/
│   ├── favicon.svg          # 브라우저 탭 아이콘
│   └── icons.svg            # 정적 아이콘 리소스
└── src/
    ├── App.css              # App 컴포넌트 전용 스타일
    ├── App.tsx              # 라우팅과 공통 레이아웃을 연결하는 앱 루트 컴포넌트
    ├── index.css            # 전역 스타일과 Tailwind 지시어
    ├── main.tsx             # React 앱을 DOM에 마운트하는 진입점
    ├── api/
    │   ├── auth.ts          # 인증 관련 API 호출 함수
    │   ├── client.ts        # 공통 API 클라이언트 설정
    │   ├── community.ts     # 커뮤니티 관련 API 호출 함수
    │   ├── postApi.ts       # 게시글 관련 API 호출 함수
    │   └── services.ts      # 서비스 기능 관련 API 호출 함수
    ├── assets/
    │   ├── hero.png         # 홈/히어로 영역에서 사용하는 이미지 리소스
    │   ├── react.svg        # React 기본 이미지 리소스
    │   └── vite.svg         # Vite 기본 이미지 리소스
    ├── components/
    │   ├── Layout.tsx       # 페이지 공통 레이아웃 컴포넌트
    │   └── Navbar.tsx       # 상단 내비게이션 컴포넌트
    └── pages/
        ├── CommunityPage.tsx  # 커뮤니티 화면
        ├── HomePage.tsx       # 홈 화면
        ├── ReportPage.tsx     # 분석/리포트 화면
        └── ServicePage.tsx    # 서비스 소개 또는 기능 화면
```

## 역할 요약

- `src/main.tsx`: React 앱의 브라우저 진입점이다.
- `src/App.tsx`: 페이지 라우팅과 공통 UI 흐름을 연결한다.
- `src/pages/`: 실제 화면 단위 컴포넌트를 둔다.
- `src/components/`: 여러 화면에서 재사용하는 공통 컴포넌트를 둔다.
- `src/api/`: 백엔드와 통신하는 API 호출 코드를 모은다.
- `public/`: 빌드 시 그대로 제공되는 정적 파일을 둔다.
