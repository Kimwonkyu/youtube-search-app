import json
import os
import sys

# 현재 디렉토리와 상위 디렉토리를 모두 추가
sys.path.insert(0, '.')
sys.path.insert(0, '..')

def handler(event, context):
    try:
        # 요청 본문 파싱
        if event.get('body'):
            request_data = json.loads(event['body'])
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({"error": "요청 본문이 필요합니다."})
            }
        
        keyword = request_data.get("keyword")
        selected_videos = request_data.get("selected_videos", [])
        
        if not keyword or not selected_videos:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({"error": "키워드와 선택된 영상이 필요합니다."})
            }
        
        # Google Sheets에 저장
        from google_sheets import save_to_google_sheets
        selected_urls = [video["url"] for video in selected_videos]
        save_to_google_sheets(keyword, selected_urls)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                "message": f"{len(selected_videos)}개의 영상이 구글 시트에 저장되었습니다."
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"error": str(e)})
        }