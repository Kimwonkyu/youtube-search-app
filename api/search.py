import json
import os
import sys
from urllib.parse import urlparse, parse_qs

# 현재 디렉토리와 상위 디렉토리를 모두 추가
sys.path.insert(0, '.')
sys.path.insert(0, '..')

def handler(event, context):
    try:
        # 쿼리 매개변수 추출
        query_params = event.get('queryStringParameters', {}) or {}
        keyword = query_params.get('keyword')
        language_filter = query_params.get('language_filter', 'korean')
        
        if not keyword:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({"error": "키워드가 필요합니다."})
            }
        
        # YouTube 검색 수행
        from youtube_search import search_youtube_links
        videos = search_youtube_links(keyword, language_filter=language_filter, max_results=200)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                "keyword": keyword,
                "videos": videos,
                "total_count": len(videos)
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