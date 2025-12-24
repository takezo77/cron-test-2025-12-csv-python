from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os, json

CSV_DIR = './csv'

# --- GitHub Actions の環境変数から token.json を生成 ---
token_env = os.getenv("GMAIL_TOKEN_JSON")
if not token_env:
    raise Exception("❌ GMAIL_TOKEN_JSON が設定されていません")

with open("token.json", "w") as f:
    f.write(token_env)

creds = Credentials.from_authorized_user_file('token.json')
service = build('drive', 'v3', credentials=creds)

# Google Drive のアップロード先フォルダ
FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")

for file_name in os.listdir(CSV_DIR):
    if file_name.endswith('.csv'):
        file_path = os.path.join(CSV_DIR, file_name)
        file_metadata = {
            'name': file_name,
            'parents': [FOLDER_ID]  # ← フォルダ指定
        }
        media = MediaFileUpload(file_path, mimetype='text/csv')

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f'✅ アップロード完了: {file_name} → ID={uploaded_file.get("id")}')
