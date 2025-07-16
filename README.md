# Youtube 키워드 영상 링크 수집 웹서비스

## 프로젝트 목적
- 유튜브에서 특정 키워드로 검색된 영상들의 링크를 수집하고, 구글 시트에 저장하는 웹서비스를 개발합니다.
- 프론트엔드는 React + Tailwind CSS, 백엔드는 FastAPI(Python)로 구현합니다.

## 전체 아키텍처
- React 프론트엔드에서 키워드 입력 → FastAPI 백엔드로 요청
- 백엔드에서 YouTube Data API로 영상 링크 수집
- 수집된 링크를 Google Sheets API로 구글 시트에 저장
- 결과를 프론트엔드에 반환 및 표시

## 사용 기술
- **백엔드:** Python, FastAPI, Uvicorn, Google API Client, python-dotenv
- **프론트엔드:** React, Tailwind CSS
- **배포:** Vercel (프론트/백엔드)

## 백엔드 구현 상태 (✅ 완료)
1. ✅ FastAPI 서버 및 CORS 설정
2. ✅ /search 엔드포인트: 키워드로 유튜브 영상 링크 20개 수집 및 구글 시트 저장
3. ✅ YouTube Data API, Google Sheets API 연동
4. ✅ 환경변수(.env), credentials.json 등 인증/보안 설정
5. ✅ 에러 처리 및 디버깅 개선
6. ✅ 한글 키워드 검색 지원

## 프론트엔드 구현 상태 (✅ 완료)
1. ✅ React 프로젝트 기본 구조 설정
2. ✅ 키워드 입력 UI 구현
3. ✅ 백엔드 API 연동 로직 구현
4. ✅ 결과 리스트 표시 컴포넌트 구현
5. ✅ 로딩 및 에러 처리 구현
6. ✅ Tailwind CSS 설정 (v3.4.14 사용하여 해결 완료)

## 환경설정 및 실행 방법
### 1. 백엔드
- Python 가상환경 생성 및 패키지 설치
- .env 파일에 API 키, 시트 ID 입력
- Google Cloud에서 credentials.json 발급 및 프로젝트 루트에 추가
- uvicorn main:app --reload 명령으로 서버 실행

### 2. 프론트엔드
- frontend 폴더로 이동: `cd frontend`
- 의존성 설치: `npm install`
- 개발 서버 실행: `npm start`
- 브라우저에서 http://localhost:3000 접속

## 현재 상태 및 테스트 방법
### ✅ 정상 동작
- **백엔드 API 서버**: `http://127.0.0.1:8000/search?keyword=발리여행`
- **프론트엔드 개발 서버**: `http://localhost:3000`
- YouTube Data API 연동 및 영상 링크 수집
- Google Sheets API 연동 및 데이터 저장
- 한글 키워드 검색 지원
- Tailwind CSS 스타일링 정상 적용

### 🧪 테스트 방법
1. **백엔드 서버 실행**: `source venv/bin/activate && uvicorn main:app --reload`
2. **프론트엔드 서버 실행**: `cd frontend && npm start`
3. **브라우저 테스트**: http://localhost:3000 접속 후 키워드 검색 테스트
4. **API 직접 테스트**: `http://127.0.0.1:8000/search?keyword=테스트키워드`

### 🔄 다음 단계
1. 전체 시스템 통합 테스트 및 UI/UX 개선
2. 배포 준비 (Vercel 등)
3. 에러 처리 및 사용자 경험 개선

## 기타
- 서비스 계정 이메일을 구글 시트에 편집자로 공유해야 저장이 정상 동작합니다.
- 자세한 개발 과정은 process.md 참고