# Trip Agency

부산·울산·경주 관광 혼잡도 기반 AI 여행 플래너의 초기 MVP입니다.
명세의 backend/frontend 구조, FastAPI 계층 분리와 React + TypeScript + Vite 화면을 구성했습니다.

## Docker 실행

```powershell
docker compose up --build
```

- 화면: http://localhost:5173
- API 문서: http://localhost:8000/docs
- 상태 API: http://localhost:8000/health

기본 설정은 `USE_MOCK_DATA=true`, `ENABLE_LLM=false`입니다. API 키 없이 샘플 관광지 탐색과 코스 추천을 사용할 수 있도록 구성했습니다.
PostgreSQL 비밀번호는 로컬 개발용 기본값입니다. `POSTGRES_PASSWORD` 환경변수로 변경할 수 있습니다.

## 로컬 실행

Python 3.11+, Node.js 22+, PostgreSQL 16을 기준으로 구성했습니다. 관광 정보가 샘플 모드여도 회원 계정과 로그인 세션 저장에는 PostgreSQL이 필요합니다.

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

새 터미널에서:

```powershell
cd frontend
npm install
npm run dev
```

## 구조

- `backend/app/api/routes`: REST API
- `backend/app/core`: 설정, DB, 로깅, 예외
- `backend/app/models`, `schemas`, `repositories`, `services`: 데이터 모델과 도메인 계층
- `backend/app/external`: 부산·울산·경주·기상청·TourAPI 연결 인터페이스
- `backend/app/ai`: 혼잡도 학습/예측, RAG, Ollama 설명, agent 도구 어댑터
- `backend/app/optimizer`: LLM과 분리된 Greedy 방문 순서 결정
- `backend/scripts`: 샘플 관광지 저장, ML 학습, 벡터 DB 구축 및 수집기 연결 지점
- `frontend/src`: 지도, 플래너, 결과 Timeline, API, hooks, store

## API

- `GET /api/v1/tourism/places?city=busan&category=sea`
- `GET /api/v1/tourism/places/{place_id}`
- `GET /api/v1/traffic/current?city=busan&place_id=1`
- `GET /api/v1/weather/current?city=busan`
- `GET /api/v1/congestion/{place_id}`
- `POST /api/v1/recommendations`
- `POST /api/v1/ai/chat` (Ollama 활성화 필요)

추천 요청 예시:

```json
{
  "start_location": "부산역",
  "start_time": "10:00",
  "end_time": "21:00",
  "cities": ["busan"],
  "preferences": ["바다", "사진"],
  "avoid_congestion": true,
  "transportation": "public",
  "must_visit": ["해운대 해수욕장"]
}
```

출발지는 부산역·울산역·경주역을 지원합니다. 다른 위치는 API에서 `start_latitude`, `start_longitude`를 함께 지정합니다.
당일 일정만 지원하며 종료지 제약, 실제 도로·버스 노선, 전역 최적해는 현재 범위에 포함되지 않습니다.
필수 관광지는 우선 선택하되 시간·운영시간 제약으로 방문하지 못하면 응답의 warnings에 표시합니다.

## Ollama / RAG

```powershell
ollama pull qwen3:8b
ollama pull qwen3-embedding:0.6b
```

로컬 backend `.env`에서 `ENABLE_LLM=true`로 설정합니다. Docker에서는 해당 환경변수를 설정하고 다시 실행합니다.
LLM에는 계산된 코스의 설명만 요청하며 연결 실패 시 코스는 기본 설명과 함께 반환합니다.
RAG 모듈은 관광 설명 Markdown을 임베딩하는 확장 기반이며 추천 흐름에는 아직 연결되지 않았습니다.
Tools는 서비스 호출용 비동기 어댑터이며 자율적인 도구 선택 agent는 후속 범위입니다.

```powershell
# backend 디렉터리에서
python -m scripts.build_vector_db ./data/documents
```

## 실제 데이터로 확장

`USE_MOCK_DATA=false`이면 DB 데이터를 조회하며 시작 시 테이블을 생성합니다. 운영 환경의 Alembic migration은 후속 작업입니다.
`python -m scripts.seed_tourism`은 **샘플 관광지**를 저장합니다. 실제 운영시간으로 대체해야 합니다.
외부 API 클라이언트는 httpx 비동기 공통 인터페이스를 제공하며 기관별 URL·인증·응답 매핑과 주기 수집은 후속 구현이 필요합니다.
교통·날씨·혼잡도가 없으면 명시적으로 데이터 없음 오류를 반환합니다.

혼잡도 학습 모듈은 LightGBM 기반으로 1·2·3시간 타깃을 별도로 학습합니다.
학습 CSV에는 `preprocessing.py`의 feature와 `future_congestion_1h`, `future_congestion_2h`, `future_congestion_3h`가 필요합니다.

```powershell
python -m scripts.train_congestion_model ./data/training.csv
```

`model.joblib`은 실제 학습 후 생성합니다. 학습 모델의 서비스 연결, 방문객 통계·공휴일 연계, 캐시, 스케줄러, 실제 예측값 저장은 후속 범위입니다.
샘플 모드는 미래 혼잡도를 생성하지 않으며 `forecast: []`를 반환합니다.
지도 타일은 OpenStreetMap에서 로드하며 추천 경로의 선은 방문 순서를 연결한 표시입니다.

## 작업 상태

사용자 요청에 따라 의존성 설치, 서버 실행, 테스트, 빌드 및 별도 검증은 수행하지 않았습니다.

## 여행 날짜와 AI 챗봇

여행 만들기 폼에서 캘린더로 날짜를 선택합니다. 한국 시간의 오늘 이후를 지원하며, `travel_date`가 추천 API 요청과 응답에 포함됩니다.
날짜별 날씨·혼잡도·휴무일 데이터는 아직 연결되지 않았으므로 현재 저장 정보로 당일 코스를 구성합니다.

상단의 **AI 챗봇**(`/chat`)은 로그인 후 이용할 수 있습니다. Ollama의 `qwen3:8b`로 이전 대화를 전달하며 답변을 생성합니다.
새 대화, Enter 전송, Shift+Enter 줄바꿈, 대기 표시 및 실패 시 재시도를 제공합니다.
대화는 페이지 메모리에 보관하며 페이지를 떠나거나 새로고침하면 초기화됩니다. 서버에 채팅 기록을 저장하지 않습니다.
최근 대화 최대 19개와 총 24,000자 이내를 모델에 전달합니다. 실시간 데이터 검색 도구는 연결되어 있지 않습니다.
`POST /api/v1/ai/chat`에 `{"messages":[{"role":"user","content":"부산 여행을 추천해 줘"}]}` 형태로 요청합니다.
기존 `{"message":"..."}` 요청도 지원합니다. 응답은 `message`, `model`이며 현재는 완성된 답변을 한 번에 반환합니다.

이번 변경에서는 로컬 `.env`의 `ENABLE_LLM=true`를 적용했습니다. Docker의 Ollama 주소는 `http://host.docker.internal:11434`입니다.
호스트 PC에서 Ollama가 실행되어 있어야 합니다. 별도 기능 테스트와 브라우저 검증은 실행하지 않았습니다.

## 만든 코스를 대화로 수정

추천 API에서 생성한 코스와 입력 조건을 로그인한 사용자의 `travel_plans` 테이블에 저장합니다.
현재 코스는 `GET /api/v1/recommendations/current`로 복원하므로 새로고침 후에도 확인할 수 있습니다.
챗봇은 클라이언트가 넘긴 임의 코스 대신 인증된 사용자의 현재 DB 코스를 읽습니다.

1. 여행 만들기에서 날짜·시간·취향을 입력하고 코스를 생성합니다.
2. 결과 화면의 **이 코스를 AI와 수정하기** 또는 상단 AI 챗봇으로 이동합니다.
3. 예: **저녁에 비가 온다는데 18시 이후를 실내 관광지로 바꿔줘**.
4. 챗봇은 Qwen3로 변경 의도·시각·제외 장소를 해석하고, optimizer가 저장된 관광지와 운영시간·이동시간으로 대체 코스를 계산합니다.
5. 변경안의 **이 코스로 변경**을 누르면 저장 코스·Timeline·지도에 적용합니다. 적용 전에는 원래 코스가 유지됩니다.

변경 시각 이전에 끝나는 방문은 유지하고, 그 시각에 걸치는 방문과 이후 방문은 다시 계획합니다.
저녁처럼 구체적인 시각이 없는 표현은 18시, 오후는 13시로 해석합니다.
우천 실내 조건은 이후 변경에도 유지합니다. 새 여행을 만들면 해당 조건도 초기화됩니다.
실내 여부는 `museum`, `aquarium`, `gallery`, `indoor` 분류만 사용하며 카페거리 전체를 실내로 취급하지 않습니다.
조건에 맞는 장소나 남은 시간이 없으면 기존 코스를 유지하고 안내합니다.

샘플 모드에는 실내 대안 시연을 위한 박물관·미술관·아쿠아리움 데이터를 추가했습니다. 운영시간은 시연용이며 실제 예보·휴무일·입장권 정보는 확인하지 않습니다.
실 데이터 모드에서는 DB에 위 실내 분류를 갖는 실제 관광지가 있어야 합니다.
변경안은 사용자별 draft로 저장하며 `POST /api/v1/recommendations/{plan_id}/apply`에서 소유자를 확인합니다.
다른 창에서 코스가 바뀌면 이전 코스의 변경안 적용은 409 오류로 차단합니다.
다른 사용자 코스는 조회하거나 수정할 수 없습니다. 채팅 메시지 자체는 아직 DB에 저장하지 않습니다.
이 기능 추가 전에 생성해 브라우저에만 남아 있던 코스는 저장 대상이 아니므로 코스를 다시 생성해야 합니다.

## 나의 여행 / 여러 코스 보관

로그인 후 상단 프로필(사용자 이름)을 누르면 **나의 여행**(`/my-travels`)으로 이동합니다.
새 코스를 만들 때마다 PostgreSQL에 별도 여행으로 자동 저장하며, 이전 여행을 덮어쓰지 않습니다.
페이지를 떠나거나 새로고침하거나 다시 로그인해도 같은 계정에서 저장한 여행 목록을 볼 수 있습니다.
이전에 DB에 저장했던 코스도 목록에 포함합니다. 적용 전 챗봇 변경안 draft는 목록에서 제외하며, 적용된 수정본과 원본은 함께 보관합니다.

- 여행 만들기 폼에서 이름을 지정할 수 있습니다. 비워두면 날짜·지역으로 기본 이름을 만듭니다.
- 나의 여행 목록, 저장 여행 상세, 추천 결과의 **이름 변경**에서 1~80자의 이름을 저장합니다.
- 목록은 한 페이지에 12개씩 표시하며 다음 페이지로 이동할 수 있습니다.
- 저장 여행 상세에서 **이 여행을 AI와 수정하기**를 누르면 해당 여행이 챗봇의 현재 코스가 됩니다. 다른 여행은 유지됩니다.
- 저장 여행의 일정·지도·안내는 `/my-travels/{plan_id}`에서 다시 볼 수 있습니다.

API는 `GET /api/v1/travels`, `GET /api/v1/travels/{plan_id}`, `PATCH /api/v1/travels/{plan_id}`(`{"title":"친구들과 부산 여행"}`),
`POST /api/v1/travels/{plan_id}/select`입니다. 모든 요청에서 JWT와 소유자를 확인합니다.
이름은 기존 JSON 데이터에 저장하므로 기존 DB 테이블의 열을 변경하지 않습니다.
사용자 요청에 따라 별도 기능 테스트·브라우저 검증은 수행하지 않았습니다.

## 프로필 메뉴와 개인 설정

로그인 후 상단 프로필을 누르면 이름·이메일과 함께 나의 여행, 찜한 장소, 여행 취향, 계정 설정, 로그아웃 메뉴가 열립니다.
바깥을 누르거나 Escape 키를 누르면 닫힙니다.

- **나의 여행**: 예정된 여행 / 지난 여행 / 전체 여행을 선택합니다. 한국 시간 기준 오늘 이상은 예정, 어제 이전은 지난 여행입니다. 서버에서 분류한 뒤 페이지 단위로 조회합니다.
- **찜한 장소**(`/favorites`): 관광지 카드의 찜 버튼으로 저장·해제합니다. 여러 장소를 선택해 새 여행의 필수 방문 장소로 넘길 수 있으며 해당 지역도 기본 선택됩니다.
- **여행 취향**(`/preferences`): 관심사, 기본 교통수단, 걷기 선호도, 혼잡도 고려 여부를 계정에 저장합니다. 새 여행 폼에 기본값으로 적용하며 이번 여행에서 개별 변경할 수 있습니다.
- **계정 설정**(`/settings`): 이름과 비밀번호를 변경합니다. 이메일은 읽기 전용입니다. 비밀번호 변경에는 현재 비밀번호가 필요하며 성공 시 모든 로그인 세션을 폐기하고 다시 로그인합니다. 여행·찜·취향 데이터는 유지합니다.

걷기 선호도는 실제 도보 경로를 계산하는 기능이 아니라 코스 순서 결정 시 장소 간 거리 비용을 조절합니다. 가까운 장소 위주를 선택하면 거리가 먼 장소의 비용을 더 크게 적용합니다.
지난 여행의 일정과 지도는 조회할 수 있지만 과거 날짜로 새 코스를 계산하지는 않습니다.

개인 설정 API는 `/api/v1/account/preferences` GET/PUT, `/profile` PATCH, `/password` POST,
`/favorites` GET, `/favorites/{place_id}` PUT/DELETE입니다. 모두 로그인한 계정의 데이터만 접근합니다.
`user_preferences`, `favorite_places` 테이블은 시작 시 추가하며 기존 회원·여행 데이터는 삭제하지 않습니다.
찜은 저장 시점의 관광지 정보를 함께 보관합니다. 이후 관광지 정보가 바뀌면 여행 생성 시 최신 관광지 조회 결과를 사용합니다.
이번 변경도 별도 테스트·브라우저 검증은 수행하지 않았습니다.

## 회원가입 / JWT 로그인

- 화면: `/register`, `/login`
- `POST /api/v1/auth/register`: `{ "email": "you@example.com", "name": "여행자", "password": "your-long-password" }`
- `POST /api/v1/auth/login`: `{ "email": "you@example.com", "password": "your-long-password" }`
- `GET /api/v1/auth/me`: 현재 사용자 조회
- `POST /api/v1/auth/logout`: 현재 로그인 세션 해제

회원가입 성공 시 자동 로그인합니다. 비밀번호는 10~128자이며 Argon2 해시로 저장합니다.
이메일은 소문자로 정규화하고 중복 가입을 차단합니다. 응답에는 비밀번호나 해시를 포함하지 않습니다.
여행지 탐색은 공개하며 코스 생성, 결과 페이지 및 AI API는 로그인 후 이용합니다.

JWT는 HS256으로 서명하며 `sub`, `jti`, `iat`, `exp`, `iss`, `aud`, `type`을 검증합니다.
기본 유효시간은 30분이고, 만료 후에는 다시 로그인합니다. refresh token은 현재 제공하지 않습니다.
브라우저에서는 JWT를 HttpOnly·SameSite=Lax 쿠키에 저장하고 `/auth/me`로 새로고침 후 로그인 상태를 복원합니다.
JWT를 localStorage나 sessionStorage에 저장하지 않습니다.
API 클라이언트는 로그인 응답의 `access_token`을 `Authorization: Bearer <token>`으로 전달할 수도 있습니다.
DB의 `auth_sessions`와 함께 확인하므로 로그아웃된 JWT는 만료 전이라도 거부합니다.
쿠키 인증으로 상태를 변경하는 요청은 허용된 Origin을 요구합니다.

`users`, `auth_sessions` 테이블은 백엔드 시작 시 생성합니다. PostgreSQL이 없으면 백엔드 시작이 실패합니다.
관광 정보 샘플 모드 여부와 사용자 저장은 별개입니다. DB만 Docker로 실행할 수도 있습니다.

```powershell
# 프로젝트 루트에서
docker compose up -d postgres

# backend 폴더에서 새 인증 의존성 설치
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`backend/.env`에는 기존 API 키를 보존하면서 무작위 `JWT_SECRET_KEY`를 추가했습니다.
프로젝트 루트 `.env`에도 Docker Compose용 비밀키를 추가했습니다. 두 파일은 Git에서 제외됩니다.
새 환경에서는 다음 명령으로 키를 생성하고 `.env.example`의 빈 항목을 채우세요. 이미 설정한 `.env`를 예제 파일로 덮어쓰지 마세요.

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

운영 HTTPS에서는 `AUTH_COOKIE_SECURE=true`와 실제 프런트엔드의 `CORS_ORIGINS`를 설정합니다.
현재 인증 구현에는 이메일 인증, 비밀번호 재설정 및 로그인 시도 횟수 제한은 포함되지 않습니다.
이번 인증 코드 변경 후 의존성 설치·테스트·빌드·실행 검증은 하지 않았습니다.
