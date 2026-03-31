import pandas as pd

# 1. 讀取檔案
df = pd.read_csv('出國旅客按首站抵達地含年齡.性別_改.csv', encoding='utf-8-sig')

# 2. 執行逆樞紐 (Unpivot)
id_cols = ['年', '月', '居住地']
df_long = pd.melt(df, id_vars=id_cols, var_name='Age_Gender_Group', value_name='Passenger_Count')

# 3. 核心清洗動作
# A. 拆分年齡與性別
df_long[['年齡層', '性別']] = df_long['Age_Gender_Group'].str.split('_', expand=True)

# B. 【關鍵修正】民國轉西元：先轉型態再加法
# pd.to_numeric 會把文字轉成數字，errors='coerce' 會把無法轉換的變為空值
df_long['年'] = pd.to_numeric(df_long['年'], errors='coerce')
df_long['年'] = df_long['年'].fillna(0).astype(int) + 1911

# C. 月份補零 (1 -> 01)
# 先轉成整數確保格式統一，再轉字串補零
df_long['月'] = pd.to_numeric(df_long['月'], errors='coerce').fillna(0).astype(int)
df_long['月'] = df_long['月'].astype(str).str.zfill(2)

# 4. 整理並儲存
final_cols = ['年', '月', '居住地', '年齡層', '性別', 'Passenger_Count']
df_final = df_long[final_cols]

# 儲存結果
df_final.to_csv('fact_Travel_Outbound_Cleaned.csv', index=False, encoding='utf-8-sig')

print("✅ 修正完成！現在年份與月份格式均符合資料庫標準。")
print(df_final.head())