import pandas as pd
import os

# 1. 設定參數
folder_path = r'C:\0324專題\260321_nNiseproj\.venv\107-114開店數exl' 
target_sheet = '表(續4)'
all_data = []

# 設定要篩選的目標值 (59 或 561, 562, 563, 569)
# 建議同時放入字串與數字，確保 Excel 格式不一時都能抓到
target_values = [56, 561, 562, 563, '56', '561', '562', '563']

# 取得檔案清單並過濾暫存檔
file_list = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls')) and not f.startswith('~$')]
file_list.sort()

if not file_list:
    print("找不到任何 Excel 檔案。")
    exit()

# --- 第一步：建立基準標題 ---
first_file_path = os.path.join(folder_path, file_list[0])
try:
    df_temp = pd.read_excel(first_file_path, sheet_name=target_sheet)
    base_columns = df_temp.columns[:5].tolist()
    print(f"✅ 基準標題：{base_columns}")
except Exception as e:
    print(f"基準檔案讀取失敗: {e}")
    exit()

# --- 第二步：遍歷處理 ---
for index, file_name in enumerate(file_list):
    file_full_path = os.path.join(folder_path, file_name)
    
    try:
        if index == 0:
            df = pd.read_excel(file_full_path, sheet_name=target_sheet)
        else:
            df = pd.read_excel(file_full_path, sheet_name=target_sheet, skiprows=6)

        # 【程序 A】：優先保留前 5 欄
        df = df.iloc[:, :5]
        df.columns = base_columns

        # 【程序 B】：核心篩選邏輯修正
        # iloc[:, 1] 是第二欄，iloc[:, 2] 是第三欄 (索引從 0 開始)
        # 使用 isin() 檢查該格數值是否在我們的目標清單中
        mask_col2 = df.iloc[:, 1].isin(target_values)
        mask_col3 = df.iloc[:, 2].isin(target_values)
        
        # 只要第二欄「或」第三欄符合，就擷取該列
        df_filtered = df[mask_col2 | mask_col3].copy()

        # 加入來源檔名
        df_filtered['來源檔案'] = file_name
        all_data.append(df_filtered)
        print(f"成功處理: {file_name} (擷取 {len(df_filtered)} 列)")

    except Exception as e:
        print(f"⚠️ 檔案 {file_name} 錯誤: {e}")

# --- 第三步：合併與匯出 ---
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    
    # 調整欄位順序：來源檔案放在最前面
    cols = ['來源檔案'] + [c for c in final_df.columns if c != '來源檔案']
    final_df = final_df[cols]
    
    output_name = '107-114開店數SQL樣式.xlsx'
    final_df.to_excel(output_name, index=False)
    print("\n" + "="*40)
    print(f"處理完成！結果已儲存至: {output_name}")
    print("="*40)
else:
    print("找不到符合條件 (59, 561-563) 的資料。")