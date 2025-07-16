import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def save_to_google_sheets(keyword, links):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    
    # 환경변수에서 Google 인증 정보 가져오기
    google_credentials = os.getenv("GOOGLE_CREDENTIALS")
    if google_credentials:
        # 환경변수에 JSON 문자열로 저장된 경우 (배포용)
        credentials_info = json.loads(google_credentials)
        creds = service_account.Credentials.from_service_account_info(
            credentials_info, scopes=SCOPES)
    else:
        # 로컬 개발용 - credentials.json 파일 사용
        SERVICE_ACCOUNT_FILE = 'credentials.json'
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    values = [[keyword, link] for link in links]
    body = {'values': values}
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="A1",
        valueInputOption="RAW",
        body=body
    ).execute() 