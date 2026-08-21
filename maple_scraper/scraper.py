import requests
import json
from datetime import datetime

def fetch_maple_data():
    # 您抓到的 API 網址
    url = "https://msapi.misaka-site.co/api/v1/maplestorytw/v1/character/batch?names=%5B%22Rainyx09%22%5D&blocks=%5B%22basic%22%2C%22stat%22%2C%22symbol-equipment%22%2C%22hexamatrix%22%2C%22propensity%22%2C%22ability%22%2C%22skill%22%2C%22item-equipment%22%2C%22android-equipment%22%2C%22link-skill%22%5D"
    
    # 偽造 Headers 模擬瀏覽器訪問
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://msapi.misaka-site.co/supervise/compare"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        # 加上時間戳記方便追蹤資料版本
        output = {
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        }
        
        # 儲存為 JSON 檔案
        filename = "character_data.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print(f"[{datetime.now()}] 資料成功抓取並存檔至 {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"抓取失敗: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_maple_data()
