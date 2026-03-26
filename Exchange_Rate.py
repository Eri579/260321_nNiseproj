import yfinance as yf
import pandas as pd

def fetch_exchange_rate():
    print("正在抓取美金-台幣匯率資料...")
    
    # 抓取 TWD=X (美金兌台幣)
    # 2026-03-26 為目前時間點
    data = yf.download("TWD=X", start="2018-01-01", end="2026-03-26")
    
    if data.empty:
        print("抓取失敗，請檢查網路連接。")
        return None

    # 只要收盤價 (Close)
    df = data[['Close']].copy()
    df.columns = ['USD_TWD']
    
    # 重設索引，將 Date 變成一般欄位
    df = df.reset_index()
    
    # 計算「月平均匯率」 (Resample)
    df_monthly = df.set_index('Date').resample('ME').mean().reset_index()
    df_monthly['Year'] = df_monthly['Date'].dt.year
    df_monthly['Month'] = df_monthly['Date'].dt.month
    
    print(f"成功取得 {len(df_monthly)} 筆月平均匯率資料！")
    return df_monthly

# 執行
exchange_df = fetch_exchange_rate()
if exchange_df is not None:
    exchange_df.to_csv('USD_TWD_Monthly.csv', index=False, encoding='utf-8-sig')
    print(exchange_df.tail())