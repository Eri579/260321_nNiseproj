import pandas as pd

# 1. 讀取檔案
file_path = 'final_summary.xlsx'
df = pd.read_excel(file_path)

# 2. 定義合併邏輯 (完全不使用欄位名稱)
def merge_logic(row):
    # .iloc[0] 代表該列的第一個格子 (原本的 A 欄)
    # .iloc[1] 代表該列的第二個格子 (原本的 B 欄)
    
    val_a = row.iloc[1]
    val_b = row.iloc[2]
    
    # 如果第二格 (B欄) 是空的，就只回傳 A
    if pd.isna(val_b):
        return val_a
    else:
        # 兩者合併，並確保轉成字串
        return str(val_a) + str(val_b)

# 3. 執行合併：將結果存入第一欄 (iloc[:, 0])
# 注意：這裡直接修改 df 的資料
df.iloc[:, 0] = df.apply(merge_logic, axis=1)

# 4. 儲存
df.to_excel('合併結果.xlsx', index=False)
print("合併完成！請查看『合併結果.xlsx』")