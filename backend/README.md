# Backend Setup

Backend는 Python 3.10, FastAPI, uvicorn을 사용한다.
가상환경과 패키지 관리는 `uv`로 통일한다.

## 처음 세팅

1. `uv` 설치 (powershell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

2. `uv`가 잘 설치됐는지 확인한다.

```powershell
uv --version
```

버전이 출력되면 정상 설치된 것이다.

3. backend 폴더로 이동한다.

```powershell
cd backend
```

4. 가상환경과 패키지를 설치한다.

```powershell
uv sync
```

이 명령은 `.python-version`, `pyproject.toml`, `uv.lock`을 기준으로 같은 Python 버전과 같은 패키지 버전을 설치한다.
생성되는 `.venv` 폴더는 개인 로컬 가상환경이므로 Git에 올리지 않는다.

## 이후 사용법

Python 파일은 `uv run`으로 실행한다.

```powershell
uv run python 파일명.py
```

테스트는 이렇게 실행한다.

```powershell
uv run pytest
```

FastAPI 서버는 앱 파일이 생긴 뒤 이렇게 실행한다.

```powershell
uv run uvicorn app.main:app --reload
```

예를 들어 `backend/app/main.py` 안에 `app = FastAPI()`가 있으면 위 명령을 사용한다.


## 패키지 추가

새 패키지를 추가할 때는 `pip install` 대신 `uv add`를 사용한다.

```powershell
uv add 패키지명
```

개발용 패키지는 `--dev` 옵션을 붙인다.

```powershell
uv add --dev 패키지명
```

패키지를 추가하면 `pyproject.toml`과 `uv.lock`이 변경된다.
이 두 파일은 팀원들이 같은 환경을 쓰기 위해 Git에 같이 올려야 한다.

## 팀원이 저장소를 받은 뒤 할 일

```powershell
cd backend
uv sync
```

그 다음부터는 `uv run ...`으로 Python, pytest, uvicorn을 실행한다.
