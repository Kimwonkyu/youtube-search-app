import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def search_youtube_links(query, language_filter="korean", max_results=200):
    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build("youtube", "v3", developerKey=api_key)
    
    all_videos = []
    next_page_token = None
    
    # 최대 200개까지 가져오기 (API 한계: 한 번에 50개씩)
    while len(all_videos) < max_results:
        remaining = min(50, max_results - len(all_videos))
        
        if language_filter == "korean":
            # 한국어 영상 우선 검색
            request = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=remaining,
                regionCode="KR",
                relevanceLanguage="ko",
                order="date",  # 최신순으로 변경
                pageToken=next_page_token
            )
        else:
            # 모든 언어 영상 검색
            request = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=remaining,
                order="date",  # 최신순으로 변경
                pageToken=next_page_token
            )
        
        response = request.execute()
        
        # 영상 ID 목록 추출
        video_ids = [item['id']['videoId'] for item in response['items']]
        
        # 조회수 정보를 가져오기 위한 추가 API 호출
        view_counts = {}
        if video_ids:
            stats_request = youtube.videos().list(
                part="statistics",
                id=",".join(video_ids)
            )
            stats_response = stats_request.execute()
            
            for stat_item in stats_response['items']:
                view_counts[stat_item['id']] = int(stat_item['statistics'].get('viewCount', 0))
        
        # 비디오 데이터 구성
        for item in response["items"]:
            video_id = item['id']['videoId']
            video_data = {
                "id": video_id,
                "title": item['snippet']['title'],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "channel": item['snippet']['channelTitle'],
                "publishedAt": item['snippet']['publishedAt'],
                "viewCount": view_counts.get(video_id, 0)
            }
            all_videos.append(video_data)
        
        # 다음 페이지 토큰 확인
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    # 게시일 최신순 우선, 같은 날짜면 조회수 순으로 정렬
    all_videos.sort(key=lambda x: (x['publishedAt'], x['viewCount']), reverse=True)
    
    return all_videos 