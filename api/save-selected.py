from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import traceback

# 상위 디렉토리를 path에 추가
sys.path.append('..')

try:
    from google_sheets import save_to_google_sheets
except ImportError:
    # Vercel 환경에서는 현재 디렉토리에서 import
    sys.path.append('.')
    from google_sheets import save_to_google_sheets

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # CORS 헤더 설정
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # 요청 본문 읽기
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            keyword = request_data.get("keyword")
            selected_videos = request_data.get("selected_videos", [])
            
            if not keyword or not selected_videos:
                response = {"error": "키워드와 선택된 영상이 필요합니다."}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # 선택된 영상들의 URL만 추출
            selected_urls = [video["url"] for video in selected_videos]
            save_to_google_sheets(keyword, selected_urls)
            
            response = {"message": f"{len(selected_videos)}개의 영상이 구글 시트에 저장되었습니다."}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"error": str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()