import pandas as pd

# 1. 讀取原始檔案
# 建議使用 utf-8-sig 以確保中文欄位名稱不亂碼
file_name = '電動車領牌數總表.csv'
try:
    df_wide = pd.read_csv(file_name, encoding='utf-8-sig')
except FileNotFoundError:
    print(f"錯誤：找不到檔案 {file_name}，請確認檔案路徑。")
    # 建立模擬資料供示範執行
    data = {
        '年': [2021, 2021], '月': [1, 2],
        'Gogoro新領牌數': [2450, 2100],
        'Tesla新領牌數': [1200, 800]
    }
    df_wide = pd.DataFrame(data)

print("--- 原始寬表格式 ---")
print(df_wide.head())

# 2. 執行 Melt (逆樞紐)
# id_vars: 保持不變的維度 (年、月)
# value_vars: 要從橫向轉為縱向的數值欄位
df_long = df_wide.melt(
    id_vars=['年', '月'], 
    value_vars=['Gogoro新領牌數', 'Tesla新領牌數'],
    var_name='品牌', 
    value_name='領牌數'
)

# 3. 資料清洗：簡化品牌名稱
# 將 "Gogoro新領牌車輛數" 取代為 "Gogoro"
# 將 "Tesla新領牌車輛數" 取代為 "Tesla"
df_long['品牌'] = df_long['品牌'].str.replace('新領牌數', '')

# 4. 排序：依照時間與品牌排序，讓資料井然有序
df_long = df_long.sort_values(by=['年', '月', '品牌']).reset_index(drop=True)

print("\n--- 轉換後長表格式 (符合資料庫正規化) ---")
print(df_long.head())

# 5. 儲存結果，準備匯入 MSSQL 或進行後續分析
output_name = '電動車領牌數_長表格_清洗後.csv'
df_long.to_csv(output_name, index=False, encoding='utf-8-sig')
print(f"\n已完成轉換！存檔名稱為: {output_name}")