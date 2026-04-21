import pandas as pd

# 1. 讀取原始檔案
file_name = 'DimDate_2000-2045_已加工.csv'
output_name = 'DimDate_2000-2045_Final.csv'

try:
    # 建議使用 utf-8-sig 以確保中文不亂碼
    df = pd.read_csv(file_name, encoding='utf-8-sig')

    # 2. 執行補零操作
    # 先轉為 int 確保去除可能的小數點（如 1.0），再轉為字串
    # 最後使用 zfill(2) 達成補零效果：1 -> 01, 10 -> 10
    df['月'] = df['月'].astype(int).astype(str).str.zfill(2)

    # 3. 預覽結果
    print("--- 補零後資料預覽 ---")
    print(df.head())

    # 4. 儲存結果
    df.to_csv(output_name, index=False, encoding='utf-8-sig')
    print(f"\n處理成功！檔案已儲存至：{output_name}")

except FileNotFoundError:
    print(f"錯誤：找不到檔案 {file_name}，請確認檔案路徑是否正確。")
except Exception as e:
    print(f"發生錯誤：{e}")