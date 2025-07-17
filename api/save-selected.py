from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
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

# Vercel에서 함수로 export
handler = app