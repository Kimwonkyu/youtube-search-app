# 개발 진행 과정 (Backend & Frontend Process)

## 1. 프로젝트 구조 및 환경설정
- Youtube/Youtube 폴더에 백엔드 코드(main.py, youtube_search.py, google_sheets.py) 작성
- Python 가상환경(venv) 생성 및 활성화
- 필수 패키지 설치: fastapi, uvicorn, google-api-python-client, google-auth, python-dotenv
- requirements.txt 작성

## 2. 환경 변수 및 인증 파일 준비
- .env 파일에 YOUTUBE_API_KEY, SPREADSHEET_ID 값 입력
- Google Cloud Console에서 서비스 계정 생성 및 credentials.json 발급
- credentials.json을 프로젝트 루트(Youtube/Youtube)에 추가
- 서비스 계정 이메일을 구글 시트에 편집자로 공유

## 3. 주요 코드 구현
- main.py: FastAPI 서버, CORS 설정, /search 엔드포인트 구현
- youtube_search.py: YouTube Data API로 영상 링크 수집 함수 구현
- google_sheets.py: Google Sheets API로 결과 저장 함수 구현

## 4. 서버 실행 및 문제 해결
- uvicorn main:app --reload 명령으로 서버 실행
- 8000번 포트 충돌 시 lsof/kill 명령으로 포트 점유 프로세스 종료
- ImportError, 문법 오류 발생 시 파일 위치 및 패키지 설치 상태 점검
- 서버 실행 후 http://127.0.0.1:8000/search?keyword=발리여행 로 API 테스트

## 5. 백엔드 추가 문제 해결 (2024-07-17)
- Google Sheets API range 매개변수 오류 해결: "Sheet1!A:B" → "A1"로 수정
- main.py에 에러 처리 및 HTTPException 추가로 디버깅 개선
- 한글 키워드 검색 테스트 성공: http://127.0.0.1:8000/search?keyword=%EB%B0%9C%EB%A6%AC%EC%97%AC%ED%96%89
- 백엔드 API 정상 동작 확인 (20개 영상 링크 수집 및 구글 시트 저장)

## 6. 프론트엔드 개발 시작 (2024-07-17)
- frontend 폴더 생성 및 React 프로젝트 초기 구조 설정
- package.json 생성 및 React 관련 패키지 설치 (react, react-dom, react-scripts)
- src/index.js, src/App.js 기본 컴포넌트 구현
- 키워드 입력, 검색 버튼, 결과 리스트 표시 기능 구현
- 백엔드 API 연동 로직 (fetch 사용)
- 로딩 상태 및 에러 처리 구현

## 7. Tailwind CSS 설정 문제 해결 (완료)
- Tailwind CSS v4 PostCSS 플러그인 구조 변경으로 인한 컴파일 오류 발생
- @tailwindcss/postcss 패키지 필요하다는 오류 메시지
- 해결: Tailwind CSS v3.4.14로 다운그레이드하여 해결 완료
- 프론트엔드 개발 서버 정상 실행 확인 (http://localhost:3000)

## 8. 프론트엔드 개발 서버 실행 성공 (2024-07-17)
- React 개발 서버 정상 실행 (http://localhost:3000)
- Tailwind CSS 스타일링 정상 적용
- 백엔드 서버와 병렬 실행 환경 구성 완료

## 9. 기타
- __pycache__ 폴더 삭제 등 캐시 문제 해결
- 파일명, 경로, 패키지 설치 등 기본 점검 반복