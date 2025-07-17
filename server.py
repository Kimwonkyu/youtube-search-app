#!/usr/bin/env python3
import os
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import traceback

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, '.')

try:
    from youtube_search import search_youtube_links
    from google_sheets import save_to_google_sheets
    MODULES_LOADED = True
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    MODULES_LOADED = False

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/search':
            self.handle_search(parsed_url.query)
        elif parsed_url.path == '/':
            self.handle_root()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        if self.path == '/save-selected':
            self.handle_save_selected()
        else:
            self.send_error(404, "Not Found")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        # Vercel 프론트엔드 도메인 허용
        origin = self.headers.get('Origin')
        if origin and (origin == 'https://youtube-search-app-henna.vercel.app' or origin.startswith('http://localhost')):
            self.send_header('Access-Control-Allow-Origin', origin)
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def handle_root(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        
        response = {
            "message": "YouTube Search API Server",
            "status": "running",
            "modules_loaded": MODULES_LOADED
        }
        self.wfile.write(json.dumps(response).encode())
    
    def handle_search(self, query_string):
        try:
            if not MODULES_LOADED:
                raise Exception("Required modules not loaded")
            
            query_params = parse_qs(query_string)
            keyword = query_params.get('keyword', [None])[0]
            language_filter = query_params.get('language_filter', ['korean'])[0]
            
            if not keyword:
                raise Exception("키워드가 필요합니다.")
            
            videos = search_youtube_links(keyword, language_filter=language_filter, max_results=200)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            
            response = {
                "keyword": keyword,
                "videos": videos,
                "total_count": len(videos)
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Search error: {e}")
            print(traceback.format_exc())
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            
            response = {"error": str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def handle_save_selected(self):
        try:
            if not MODULES_LOADED:
                raise Exception("Required modules not loaded")
            
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            keyword = request_data.get("keyword")
            selected_videos = request_data.get("selected_videos", [])
            
            if not keyword or not selected_videos:
                raise Exception("키워드와 선택된 영상이 필요합니다.")
            
            selected_urls = [video["url"] for video in selected_videos]
            save_to_google_sheets(keyword, selected_urls)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            
            response = {"message": f"{len(selected_videos)}개의 영상이 구글 시트에 저장되었습니다."}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Save error: {e}")
            print(traceback.format_exc())
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            
            response = {"error": str(e)}
            self.wfile.write(json.dumps(response).encode())

def run_server():
    port = int(os.getenv('PORT', 8000))
    
    print(f"🚀 Starting server on port {port}")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    print(f"📦 Modules loaded: {MODULES_LOADED}")
    
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    
    try:
        print(f"✅ Server running at http://0.0.0.0:{port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        server.server_close()

if __name__ == '__main__':
    run_server()