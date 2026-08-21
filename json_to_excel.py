import json
import pandas as pd

def process_data():
    # 讀取爬蟲抓下來的 JSON
    with open("character_data.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
    
    events = json_data.get("events", [])
    
    # 準備用來存放各分頁資料的字典
    sheets_data = {
        "綜合_Basic": [],
        "能力值_Stat": [],
        "ARC_AUT": [],
        "HEXA進度": [],
        "性向_Propensity": [],
        "內潛_Ability": [],
        "技能_Skill": [],
        "裝備_Equipment": []
    }

    # 解析並分類 JSON 區塊
    for event in events:
        if event.get("type") == "block":
            block_name = event.get("name")
            data = event.get("data", {})
            
            # 根據區塊名稱 (block_name) 將資料分配到對應的分頁
            if block_name == "basic":
                sheets_data["綜合_Basic"].append(pd.json_normalize(data))
            elif block_name == "stat":
                sheets_data["能力值_Stat"].append(pd.json_normalize(data))
            elif block_name == "symbol-equipment":
                sheets_data["ARC_AUT"].append(pd.json_normalize(data))
            elif block_name == "hexamatrix":
                sheets_data["HEXA進度"].append(pd.json_normalize(data))
            elif block_name == "propensity":
                sheets_data["性向_Propensity"].append(pd.json_normalize(data))
            elif block_name == "ability":
                sheets_data["內潛_Ability"].append(pd.json_normalize(data))
            elif block_name == "skill":
                sheets_data["技能_Skill"].append(pd.json_normalize(data))
            elif block_name in ["item-equipment", "android-equipment"]:
                # 將角色裝備與機器人裝備放在同一頁
                sheets_data["裝備_Equipment"].append(pd.json_normalize(data))

    # 將資料寫入 Excel (包含多個工作表)
    with pd.ExcelWriter("character_data_formatted.xlsx", engine="openpyxl") as writer:
        for sheet_name, df_list in sheets_data.items():
            if df_list:
                # 把串列中的 dataframe 合併成一個
                combined_df = pd.concat(df_list, ignore_index=True)
                combined_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
    print("資料已成功攤平並轉換為 character_data_formatted.xlsx！")

if __name__ == "__main__":
    process_data()
