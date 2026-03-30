import yfinance as yf
import os

save_dir = "./data/stock_data" 
file_name = "GRMN_2018_2026.csv"
full_path = os.path.join(save_dir, file_name)


os.makedirs(save_dir, exist_ok=True)

ticker = yf.Ticker("GRMN")
df = ticker.history(start="2018-01-01", end="2026-12-31")

df.to_csv(full_path, encoding="utf-8-sig")
print(f"✅ 檔案已成功儲存至: {full_path}")