import os
import googleapiclient.discovery
import googleapiclient.errors
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def search_youtube(keyword):
    # YouTube APIの初期化
    api_service_name = "youtube"
    api_version = "v3"
    youtube_api_key = ""  # YouTube APIキーを設定

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=youtube_api_key)

    # 検索クエリの実行
    request = youtube.search().list(
        part="snippet",
        maxResults=3,
        q=keyword,
        type="video"  # 動画のみを検索するために追加
    )
    response = request.execute()

    # 上位3つの動画URLの取得
    urls = []
    for item in response.get("items", []):
        if item["id"]["kind"] == "youtube#video":  # 動画アイテムであることを確認
            video_id = item["id"]["videoId"]
            urls.append(f"https://www.youtube.com/watch?v={video_id}")

    return urls

def output_to_spreadsheet(urls, spreadsheet_id):
    # スプレッドシートAPIの初期化
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("./path_to_your_credentials.json", scopes) # JSONファイルパスを指定　※path_to_your_credentials.jsonはプレースホルダー
    client = gspread.authorize(creds)

    # スプレッドシートへの書き込み
    sheet = client.open_by_key(spreadsheet_id).sheet1
    for i, url in enumerate(urls):
        sheet.update_cell(i + 1, 1, url)

def main():
    keyword = "" # 検索キーワード
    spreadsheet_id = ""  # スプレッドシートIDを設定

    # YouTubeでキーワード検索
    urls = search_youtube(keyword)

    # スプレッドシートに出力
    output_to_spreadsheet(urls, spreadsheet_id)

if __name__ == "__main__":
    main()
