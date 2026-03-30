import pandas as pd

# 讀取你剛剛產出的 CSV
df = pd.read_csv('Transformed_Quarterly_Data.csv', encoding='utf-8-sig')

def clean_summary_rows(df):
    # 1. 處理「全國」總計：刪除 縣市 為 '全國' 的列
    df = df[df['縣市'] != '全國']
    
    # 2. 處理「縣市總計」：
    # 觀察圖片，縣市總計的那一列，'鄉鎮市區' 是空白的
    # 我們使用 .dropna(subset=['鄉鎮市區']) 來刪除鄉鎮市區為空的列
    df = df.dropna(subset=['鄉鎮市區'])
    
    # 3. 如果 '鄉鎮市區' 欄位在 CSV 裡是空字串而非 NaN，請改用這行：
    # df = df[df['鄉鎮市區'].str.strip() != '']
    
    return df

# 執行清洗
df_refined = clean_summary_rows(df)

# 匯出最終版，準備進入 MSSQL
df_refined.to_csv('Housing_Detail_Data.csv', index=False, encoding='utf-8-sig')

print(f"清洗完成！剩餘筆數：{len(df_refined)} 筆（已移除全國與縣市總計層級）")