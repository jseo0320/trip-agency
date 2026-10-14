# Trip Agency Backend

실행 방법과 API, 후속 연동 범위는 루트 README를 참고하세요.

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

관광 정보 샘플 모드에서도 회원 계정과 JWT 로그인 세션 저장을 위해 PostgreSQL 연결이 필요합니다.
실행 전에 `.env`의 `DATABASE_URL`과 `JWT_SECRET_KEY`를 설정하세요. JWT 비밀키는 최소 32바이트가 필요합니다.
`tests/`는 명세의 폴더 구조를 위한 디렉터리이며 테스트를 작성하거나 실행하지 않았습니다.
