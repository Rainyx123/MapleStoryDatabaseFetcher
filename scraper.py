import requests
import json
from datetime import datetime

def fetch_maple_data():
    url = "https://msapi.misaka-site.co/api/v1/maplestorytw/v1/character/batch"
    
    # 將原本網址帶的參數拆出來寫在 dict 裡
    params = {
        'names': '["Rainyx09"]',
        'blocks': '["basic","stat","symbol-equipment","hexamatrix","propensity","ability","skill","item-equipment","android-equipment","link-skill"]'
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://msapi.misaka-site.co/supervise/compare"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 為了除錯：先印出前 200 個字元確認是不是 JSON
        print("Response text preview:", response.text[:200])
        
        data = response.json()
        
        output = {
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        }
        
        with open("character_data.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
        print("資料成功抓取並存檔")
        
    except requests.exceptions.RequestException as e:
        print(f"請求失敗: {e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失敗，伺服器回傳的不是 JSON。內容為: {response.text}")
        exit(1)

if __name__ == "__main__":
    fetch_maple_data()
