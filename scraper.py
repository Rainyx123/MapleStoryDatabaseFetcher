import requests
import json
from datetime import datetime
from sseclient import SSEClient

def fetch_maple_data():
    url = "https://msapi.misaka-site.co/api/v1/maplestorytw/v1/character/batch"
    
    params = {
        'names': '["Rainyx09"]',
        'blocks': '["basic","stat","symbol-equipment","hexamatrix","propensity","ability","skill","item-equipment","android-equipment","link-skill"]'
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://msapi.misaka-site.co/supervise/compare",
        "Accept": "text/event-stream"  # 告訴伺服器我們準備接收 SSE
    }
    
    print("開始連線並接收資料...")
    
    # 建立一個 list 來儲存所有接收到的區塊資料
    collected_data = []
    
    try:
        # stream=True 是 SSE 的關鍵
        response = requests.get(url, params=params, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        # 使用 SSEClient 解析資料流
        client = SSEClient(response)
        
        for event in client.events():
            if event.data:
                # 解析每一筆回傳的 JSON
                block_data = json.loads(event.data)
                print(f"收到資料類型: {block_data.get('type')}")
                collected_data.append(block_data)
                
                # 判斷是否結束 (假設 API 最後會傳一個結束標記，若沒有，可能需要依賴超時或特定的 type)
                if block_data.get("type") == "character_end" or block_data.get("type") == "batch_end":
                    print("資料接收完畢，主動斷開連線。")
                    break
                    
    except requests.exceptions.RequestException as e:
        print(f"連線失敗: {e}")
        exit(1)
    except Exception as e:
        # 捕捉其他潛在錯誤
        print(f"處理資料流時發生錯誤: {e}")
        # 即使報錯，也試著保存已收到的資料

    # 組合最終要儲存的資料結構
    output = {
        "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "events": collected_data
    }
    
    with open("character_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
        
    print(f"共抓取 {len(collected_data)} 筆區塊資料，並已存檔。")

if __name__ == "__main__":
    fetch_maple_data()
