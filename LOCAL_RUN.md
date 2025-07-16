# 로컬 실행 가이드

## 🚀 자동 실행 (추천)

```bash
./start-local.sh
```

## 🔧 수동 실행

### 1단계: 백엔드 서버 실행
```bash
# 가상환경 활성화
source venv/bin/activate

# 백엔드 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2단계: 프론트엔드 서버 실행 (새 터미널)
```bash
# React 개발 서버 실행
npm start
```

## 📱 접속 URL

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 🔍 테스트 방법

1. http://localhost:3000 접속
2. 키워드 입력 (예: "발리여행")
3. 언어 선택 (한국어 우선 / 상관없이 모두)
4. 검색 버튼 클릭
5. 결과 확인 및 선택
6. "구글 시트에 저장" 버튼 클릭

## 🛑 서버 종료

- **자동 실행한 경우**: 터미널에서 Enter 키
- **수동 실행한 경우**: Ctrl+C

## 🔧 문제 해결

### 포트 충돌 시
```bash
# 8000 포트 사용 프로세스 확인
lsof -ti:8000 | xargs kill -9

# 3000 포트 사용 프로세스 확인  
lsof -ti:3000 | xargs kill -9
```

### 의존성 문제 시
```bash
# 백엔드 의존성 재설치
pip install -r requirements.txt

# 프론트엔드 의존성 재설치
npm install
```