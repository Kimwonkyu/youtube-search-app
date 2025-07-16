# 배포 가이드

## 🔐 보안 설정

### 1. 환경변수 준비
다음 정보들을 각 배포 플랫폼의 환경변수로 설정해야 합니다:

#### 백엔드 (Railway)
- `YOUTUBE_API_KEY`: YouTube Data API 키
- `SPREADSHEET_ID`: Google Sheets ID
- `GOOGLE_CREDENTIALS`: Google 서비스 계정 JSON (한 줄로 압축)
- `ENVIRONMENT`: production

#### 프론트엔드 (Vercel)
- `REACT_APP_API_URL`: 백엔드 API URL (예: https://your-app.railway.app)

### 2. Google 서비스 계정 JSON 압축 방법
```bash
# credentials.json 파일 내용을 한 줄로 압축
cat credentials.json | tr -d '\n' | tr -d ' '
```

## 🚀 배포 단계

### 1단계: GitHub 저장소 준비
```bash
# 1. Git 초기화
git init
git add .
git commit -m "Initial commit"

# 2. GitHub 저장소 생성 후 연결
git remote add origin https://github.com/yourusername/youtube-search-app.git
git push -u origin main
```

### 2단계: Railway 백엔드 배포
1. https://railway.app 접속
2. GitHub 계정으로 로그인
3. "New Project" → "Deploy from GitHub repo"
4. 저장소 선택
5. 환경변수 설정:
   - `YOUTUBE_API_KEY`
   - `SPREADSHEET_ID` 
   - `GOOGLE_CREDENTIALS`
   - `ENVIRONMENT=production`
6. 자동 배포 완료

### 3단계: Vercel 프론트엔드 배포
1. https://vercel.com 접속
2. GitHub 계정으로 로그인
3. "New Project" → 저장소 선택
4. Root Directory: `frontend`
5. 환경변수 설정:
   - `REACT_APP_API_URL`: Railway에서 제공한 백엔드 URL
6. 자동 배포 완료

### 4단계: CORS 설정 업데이트
Railway 배포 완료 후 `main.py`에서 프론트엔드 도메인을 실제 Vercel 도메인으로 변경:
```python
allowed_origins = [
    "https://your-app.vercel.app",  # 실제 Vercel 도메인
    "https://localhost:3000"
]
```

## 📝 주의사항

### 보안
- ⚠️ **credentials.json 파일 절대 GitHub에 올리지 말 것**
- ⚠️ **API 키들 환경변수로만 관리**
- ⚠️ **CORS 설정을 프로덕션 도메인으로 제한**

### 테스트
- 로컬에서 테스트 후 배포
- 환경변수 설정 확인
- API 연결 테스트

## 🔧 트러블슈팅

### 공통 문제
- **CORS 오류**: 백엔드 allowed_origins에 프론트엔드 도메인 추가
- **환경변수 오류**: 플랫폼별 환경변수 설정 확인
- **API 연결 오류**: REACT_APP_API_URL 확인

### Railway 관련
- 빌드 실패: requirements.txt 확인
- 포트 오류: Procfile 확인

### Vercel 관련  
- 빌드 실패: package.json 확인
- API 연결 실패: 환경변수 확인