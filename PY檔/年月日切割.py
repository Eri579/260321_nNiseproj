import pandas as pd

# 1. 讀取 CSV 檔案
# 建議加上 encoding='utf-8-sig' 以確保中文不亂碼
file_name = 'fact_EggsPrice.csv'
df = pd.read_csv(file_name, encoding='utf-8-sig')

# 2. 強制轉換「日期」欄位為 datetime 物件
# dayfirst=False 是台灣常見的 YYYY/MM/DD 格式，errors='coerce' 會處理異常格式
df['日期'] = pd.to_datetime(df['日期'], errors='coerce')

# 3. 執行拆分：新增 年、月、日 獨立欄位
# 使用 .dt 存取器提取數值
df['年'] = df['日期'].dt.year
df['月'] = df['日期'].dt.month
df['日'] = df['日期'].dt.day

# 4. 資料清理補強（選配）
# 拆分後如果日期欄位有空值(NaT)，轉換出來的年、月、日會變成 float (例如 2023.0)
# 我們可以填補 0 並轉回整數，方便資料庫存儲
df[['年', '月', '日']] = df[['年', '月', '日']].fillna(0).astype(int)

# 5. 調整欄位順序（讓年、月、日出現在日期後面，方便視覺檢查）
cols = list(df.columns)
# 這裡假設你的原始日期欄位在前面，我們重新排列
# 你也可以跳過這步，直接儲存
print("處理後的欄位清單：", df.columns.tolist())

# 6. 匯出新的 CSV 檔案
output_name = 'fact_EggsPrice_Processed.csv'
df.to_csv(output_name, index=False, encoding='utf-8-sig')

print(f"✅ 檔案已成功處理並儲存為: {output_name}")
print(df[['日期', '年', '月', '日']].head())