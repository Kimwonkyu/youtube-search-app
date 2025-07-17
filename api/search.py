from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import sys
import traceback

# 상위 디렉토리를 path에 추가
sys.path.append('..')

try:
    from youtube_search import search_youtube_links
except ImportError:
    # Vercel 환경에서는 현재 디렉토리에서 import
    sys.path.append('.')
    from youtube_search import search_youtube_links

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # CORS 헤더 설정
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # URL 파싱
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            keyword = query_params.get('keyword', [None])[0]
            language_filter = query_params.get('language_filter', ['korean'])[0]
            
            if not keyword:
                response = {"error": "키워드가 필요합니다."}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # YouTube 검색 수행
            videos = search_youtube_links(keyword, language_filter=language_filter, max_results=200)
            response = {"keyword": keyword, "videos": videos, "total_count": len(videos)}
            
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