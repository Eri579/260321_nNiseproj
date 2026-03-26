import yfinance as yf
import os
import pandas as pd

ticker_symbol = "1476.TW"  
start_date = "2018-01-01"
end_date = "2026-12-31"

save_dir = "C:\Project"
file_name = "Eclat_1476_2018_2026.csv"
full_path = os.path.join(save_dir, file_name)

# 確保資料夾存在
os.makedirs(save_dir, exist_ok=True)


print(f"正在從 Yahoo Finance 抓取 {ticker_symbol} 的數據...")
# auto_adjust=True: 自動處理除權息（還原股價），對分析長期走勢最精準
df = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=True)


if not df.empty:
    df.to_csv(full_path, encoding="utf-8-sig")
    print("-" * 30)
    print(f"抓取成功！")
    print(f"存檔路徑: {full_path}")
    print(f"資料筆數: {len(df)} 筆")
    print(f"資料期間: {df.index.min().date()} 至 {df.index.max().date()}")
    print("-" * 30)
    print(df.head())
else:
    print("抓取失敗，請檢查網路連線或股票代碼是否正確。")