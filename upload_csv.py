from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os

# token.json を使って認証
creds = Credentials.from_authorized_user_file('token.json')

# Drive API サービス作成
service = build('drive', 'v3', credentials=creds)

# CSV フォルダ内の全ファイルをアップロード
CSV_DIR = './csv'

for file_name in os.listdir(CSV_DIR):
    if file_name.endswith('.csv'):
        file_path = os.path.join(CSV_DIR, file_name)
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, mimetype='text/csv')
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f'アップロード完了: {file_name}, File ID: {uploaded_file.get("id")}')
