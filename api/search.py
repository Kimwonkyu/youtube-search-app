from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def search(keyword: str = Query(...), language_filter: str = Query("korean")):
    try:
        videos = search_youtube_links(keyword, language_filter=language_filter, max_results=200)
        return {"keyword": keyword, "videos": videos, "total_count": len(videos)}
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# Vercel에서 함수로 export
handler = app