#!/bin/bash

echo "🚀 YouTube Search App 로컬 실행 스크립트"
echo "=================================="

# 백엔드 서버 실행
echo "📡 백엔드 서버 시작 중..."
cd /Users/wonkyukim/PythonWorkspace/Youtube/Youtube
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "✅ 백엔드 서버 시작됨 (PID: $BACKEND_PID)"
echo "🔗 백엔드 URL: http://localhost:8000"

# 잠깐 기다리기
sleep 3

# 프론트엔드 서버 실행 (React 18 버전)
echo "⚛️ 프론트엔드 서버 시작 중..."
cd /Users/wonkyukim/PythonWorkspace/Youtube/Youtube
npm start &
FRONTEND_PID=$!

echo "✅ 프론트엔드 서버 시작됨 (PID: $FRONTEND_PID)"
echo "🔗 프론트엔드 URL: http://localhost:3000"

echo ""
echo "🎉 모든 서버가 실행되었습니다!"
echo "📱 브라우저에서 http://localhost:3000 을 열어보세요"
echo ""
echo "🛑 서버 종료 방법:"
echo "   Ctrl+C 또는 다음 명령 실행:"
echo "   kill $BACKEND_PID $FRONTEND_PID"

# 사용자 입력 대기
echo ""
echo "종료하려면 Enter 키를 누르세요..."
read

# 서버 종료
echo "🛑 서버들을 종료하고 있습니다..."
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo "✅ 모든 서버가 종료되었습니다."