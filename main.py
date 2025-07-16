from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from youtube_search import search_youtube_links
from google_sheets import save_to_google_sheets
import traceback

load_dotenv()

app = FastAPI()

# 환경에 따른 CORS 설정
allowed_origins = ["*"]  # 개발용
if os.getenv("ENVIRONMENT") == "production":
    allowed_origins = [
        "https://your-frontend-domain.vercel.app",  # 실제 프론트엔드 도메인으로 변경
        "https://localhost:3000"  # 로컬 개발용
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(keyword: str = Query(...), language_filter: str = Query("korean")):
    try:
        videos = search_youtube_links(keyword, language_filter=language_filter, max_results=200)
        return {"keyword": keyword, "videos": videos, "total_count": len(videos)}
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-selected")
def save_selected_videos(request: dict):
    try:
        keyword = request.get("keyword")
        selected_videos = request.get("selected_videos", [])
        
        if not keyword or not selected_videos:
            raise HTTPException(status_code=400, detail="키워드와 선택된 영상이 필요합니다.")
        
        # 선택된 영상들의 URL만 추출
        selected_urls = [video["url"] for video in selected_videos]
        save_to_google_sheets(keyword, selected_urls)
        
        return {"message": f"{len(selected_videos)}개의 영상이 구글 시트에 저장되었습니다."}
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e)) 