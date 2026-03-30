import yfinance as yf
import pandas as pd
import os

# 1. 設定參數
股票代碼 = "2330.TW"
開始日期 = "2010-01-01"
儲存路徑 = r"C:\0326專題\2330_history_2010_2026.csv"

# 確保資料夾存在
os.makedirs(os.path.dirname(儲存路徑), exist_ok=True)

try:
    print(f"正在抓取 {股票代碼} 從 {開始日期} 至今的資料...")
    
    # 2. 抓取資料 (auto_adjust=True 會自動處理除權息，反映還原股價)
    df = yf.download(股票代碼, start=開始日期, auto_adjust=True)
    
    if not df.empty:
        # 3. 儲存資料
        # index=True 是因為 yfinance 的日期在 Index，必須保留才能進入資料庫
        df.to_csv(儲存路徑, encoding='utf-8-sig')
        print(f"成功！檔案已儲存至：{儲存路徑}")
        print(f"資料筆數：{len(df)} 筆")
    else:
        print("抓取失敗，請檢查網路連線或股票代碼。")

except Exception as e:
    print(f"錯誤發生：{e}")