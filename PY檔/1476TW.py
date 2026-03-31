import yfinance as yf
import os
import pandas as pd

# 1. 基本參數設定
ticker_symbol = "1476.TW"  
start_date = "2018-01-01"
end_date = "2026-12-31"

# 使用 r'' 避免 Windows 路徑錯誤
save_dir = r"C:\Project"
file_name = "Eclat_1476_2018_2026.csv"
full_path = os.path.join(save_dir, file_name)

os.makedirs(save_dir, exist_ok=True)

print(f"正在從 Yahoo Finance 抓取 {ticker_symbol} 的數據...")

# 2. 下載數據
# auto_adjust=True 得到的是「還原股價」，這對於分析長期「投資報酬相關性」最正確
df = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=True)

if not df.empty:
    # --- 關鍵修正區：處理 yfinance 新版的 MultiIndex 標頭 ---
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0) 
    
    # 重設索引，讓 Date 變成一般欄位，方便 SQL 辨識
    df = df.reset_index()
    
    # 新增識別標籤，方便未來多表合併
    df['Ticker'] = "1476"
    df['Stock_Name'] = "儒鴻"
    
    # 3. 存檔
    df.to_csv(full_path, index=False, encoding="utf-8-sig")
    
    print("-" * 30)
    print(f"抓取成功！")
    print(f"存檔路徑: {full_path}")
    print(f"資料筆數: {len(df)} 筆")
    print("-" * 30)
    print(df.head())
else:
    print("抓取失敗，請檢查代碼或網路。")