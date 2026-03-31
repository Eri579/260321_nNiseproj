import yfinance as yf
import os
import pandas as pd

# 1. 參數設定
ticker_symbol = "1476.TW"  # 儒鴻
start_date = "2018-01-01"
end_date = "2026-12-31"

# 使用 r'' 避免 Windows 路徑轉義字元錯誤
save_dir = r"C:\Project"
file_name = "Eclat_1476_Raw_Price.csv"
full_path = os.path.join(save_dir, file_name)

# 確保資料夾存在
os.makedirs(save_dir, exist_ok=True)

print(f"正在從 Yahoo Finance 抓取 {ticker_symbol} 的原始市場數據...")

# 2. 下載數據：auto_adjust=False 代表抓取原始報價
df = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=False)

if not df.empty:
    # --- 關鍵處理區 ---
    # A. 處理 yfinance 可能產生的 MultiIndex 標頭 (新版常見問題)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # B. 移除 'Adj Close' 欄位，只保留原始 Open, High, Low, Close, Volume
    if 'Adj Close' in df.columns:
        df = df.drop(columns=['Adj Close'])
    
    # C. 將索引 (Date) 轉為一般欄位
    df = df.reset_index()
    
    # D. 補上股票識別標籤，方便未來在 SQL 中區分
    df['Ticker'] = "1476"
    df['Stock_Name'] = "儒鴻"

    # E. 數值微調：原始報價通常只到小數點下一位 (如 .5)，進行精簡
    price_cols = ['Open', 'High', 'Low', 'Close']
    df[price_cols] = df[price_cols].round(2)
    
    # 3. 儲存 CSV
    df.to_csv(full_path, index=False, encoding="utf-8-sig")
    
    print("-" * 30)
    print(f"抓取成功！檔案已存至: {full_path}")
    print(f"目前欄位: {list(df.columns)}")
    print(f"資料筆數: {len(df)} 筆")
    print(f"最新的五筆數據：")
    print(df.tail())
    print("-" * 30)
else:
    print("抓取失敗，請檢查網路連線或代碼是否正確。")