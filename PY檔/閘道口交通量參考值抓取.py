import os
import pandas as pd
import glob

# 1. 設定路徑
input_folder = r"C:\0324專題\260321_nNiseproj\.venv\匝道交通數量"  # CSV 檔案所在的資料夾
output_file = "合併後的交通量總表.csv" # 建議存成 CSV，相容性最高

# 2. 取得所有 CSV 檔案路徑
file_list = glob.glob(os.path.join(input_folder, "*.csv"))

all_data = []

print(f"找到 {len(file_list)} 個 CSV 檔案，開始處理...")

for file_path in file_list:
    file_name = os.path.basename(file_path)
    
    # 提取檔名前 4 個字 (例如: 112年)
    prefix = file_name[:4]
    
    try:
        # 讀取 CSV
        # encoding='utf-8-sig' 可以處理包含 BOM 的中文檔案
        # 如果執行時報碼錯誤，請嘗試改用 encoding='cp950'
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        # --- 核心邏輯：在第一欄插入檔名前4字 ---
        df.insert(0, '年度標籤', prefix)
        
        all_data.append(df)
        print(f"已讀取: {file_name} (前4字: {prefix})")

    except Exception as e:
        # 處理編碼錯誤的備案
        try:
            df = pd.read_csv(file_path, encoding='cp950')
            df.insert(0, '年度標籤', prefix)
            all_data.append(df)
            print(f"已讀取(cp950): {file_name}")
        except:
            print(f"跳過檔案 {file_name}，錯誤原因: {e}")

# 3. 合併所有資料
if all_data:
    print("\n正在合併所有資料中...")
    # ignore_index=True 會重整所有編號
    final_df = pd.concat(all_data, ignore_index=True)
    
    # 4. 儲存結果
    # index=False 代表不儲存左邊那排 0, 1, 2... 的數字
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("---")
    print(f"合併完成！共合併 {len(all_data)} 個檔案。")
    print(f"最終資料列數: {len(final_df)}")
    print(f"結果存檔於: {output_file}")
else:
    print("錯誤：沒有成功讀取任何資料。")