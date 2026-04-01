import pandas as pd
import re
import os

# 1. 設定檔案路徑
input_file = '縣市人口資料含北中南區域彙整_清洗後.csv'
output_file = '縣市人口資料_純中文版_Final.csv'

def clean_city_data(file_path):
    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        print(f"找不到檔案：{file_path}，請確認檔案放在相同資料夾。")
        return

    # 讀取資料 (考慮到台灣常用編碼，若報錯可嘗試 encoding='big5' 或 'utf-8-sig')
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except:
        df = pd.read_csv(file_path, encoding='big5')

    print("--- 原始資料預覽 ---")
    print(df.head())

    # 2. 定義核心清洗邏輯
    # 使用正規表達式只保留中文：\u4e00-\u9fa5 是中文字碼範圍
    def extract_chinese(text):
        if pd.isna(text):
            return text
        # 移除英文、數字、括號及空格
        cleaned = re.sub(r'[^\u4e00-\u9fa5]', '', str(text))
        return cleaned

    # 3. 執行清洗：假設欄位名稱為 '名稱' (請根據你檔案實際欄位名調整)
    target_column = '名稱' 
    
    if target_column in df.columns:
        # 去除英文與雜訊
        df[target_column] = df[target_column].apply(extract_chinese)
        
        # 數據標準化：統一將「臺」改為「台」
        # 這是為了方便後續 JOIN 內政部(住)與大成/卜蜂(食)的資料
        df[target_column] = df[target_column].str.replace('臺', '台')
        
        print(f"\n--- '{target_column}' 欄位清洗完成 ---")
    else:
        print(f"錯誤：找不到欄位 '{target_column}'，請檢查 CSV 標題。")
        return

    # 4. 資料品質檢查 (Quality Check)
    # 檢查是否有清洗後變為空值的狀況
    empty_rows = df[df[target_column] == ''].shape[0]
    if empty_rows > 0:
        print(f"警告：有 {empty_rows} 筆資料清洗後為空，請確認原始格式。")

    # 5. 儲存結果
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n清洗成功！已儲存至：{output_file}")
    print(df.head())

# 執行程式
if __name__ == "__main__":
    clean_city_data(input_file)