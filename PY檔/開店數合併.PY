import pandas as pd
import os

# 1. 設定資料夾路徑與目標工作表名稱
folder_path = r'.\107-114開店數exl'  # 存放多個 Excel 檔案的資料夾
target_sheet = '表(續4)'      # 你要擷取的特定分頁名稱
all_data = []                   # 用來存放每個檔案資料的列表

# 2. 遍歷資料夾中的所有檔案
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        file_full_path = os.path.join(folder_path, file_name)
        
        # 讀取特定工作表
        df = pd.read_excel(file_full_path, sheet_name=target_sheet)
        
        # (選擇性) 加入一欄紀錄來源檔名，方便追蹤
        df['來源檔案'] = file_name
        
        # 將讀取的資料加入列表
        all_data.append(df)

# 3. 垂直合併所有資料
combined_df = pd.concat(all_data, ignore_index=True)

# 4. 這裡可以進行你需要的「彙整到新欄」操作
# 例如：計算新欄位
#combined_df['新彙整欄位'] = combined_df['某個數值欄位'] * 1.05 

# 5. 儲存成一個最終的總表
combined_df.to_excel('final_summary.xlsx', index=False)

print(f"已成功合併 {len(all_data)} 個檔案！")