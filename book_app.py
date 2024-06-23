from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Googleスプレッドシートの認証
def authenticate_google_docs():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    # サービスアカウントのJSONファイルキーのパスを指定
    creds = ServiceAccountCredentials.from_json_keyfile_name('goto-books-project-f4eb1a3c3a60.json', scope)
    client = gspread.authorize(creds)
    return client

@app.route('/')
def index():
    client = authenticate_google_docs()
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1K9aJxB0sjrETjSpE297mniL_l1IbQtZWxiNL-uvFB70/edit#gid=0').sheet1
    books = sheet.get_all_records()  # 全データを辞書のリストとして取得
    return render_template('layout.html', books=books)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
    #app.run(debug=True) 