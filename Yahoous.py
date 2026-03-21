import yfinance as yf
import pandas as pd

股票代碼 = "2330.TW"
資料 = yf.download(股票代碼, start="2010-01-01")
data.to_csv("TSMC_history_2010_2026_US.csv")
