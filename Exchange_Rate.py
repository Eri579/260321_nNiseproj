import yfinance as yf
import pandas as pd
import os

def export_exchange_rate_to_csv(filename="USD_TWD_Daily.csv"):
    # 1. 抓取數據
    ticker = "TWD=X"
    print(f"正在從 Yahoo Finance 抓取 {ticker} 數據...")
    df = yf.download(ticker, start="2018-01-01", end="2026-03-31")
    
    # 2. 資料清理與格式化
    df = df[['Close']].reset_index()
    df.columns = ['Date', 'ExchangeRate']
    
    # 確保日期格式為 YYYY-MM-DD (MSSQL 最友善格式)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    # 處理可能的遺漏值 (前向填充)
    df['ExchangeRate'] = df['ExchangeRate'].ffill()
    
    # 3. 匯出 CSV
    # index=False 避免多出一欄無意義的編號
    # encoding='utf-8-sig' 確保 Excel 開啟時中文不亂碼 (若未來加入中文欄位名)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"匯出完成！檔案路徑: {os.path.abspath(filename)}")
    print(f"總筆數: {len(df)} 筆")

# 執行
export_exchange_rate_to_csv()