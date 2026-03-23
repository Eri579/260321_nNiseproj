import csv
import time
import random
import pymssql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# --- 資料庫設定區 ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'Admin',
    'password': '0000',
    'database': '即時股票'
}

TABLE_NAME = "[TSMC_2330]"

def convert_to_ad_date(roc_date_str):
    """將民國年轉換為西元年 (例如: 113/01/01 -> 2024/01/01)"""
    try:
        parts = roc_date_str.split('/')
        if len(parts) == 3:
            ad_year = int(parts[0]) + 1911
            return f"{ad_year}/{parts[1]}/{parts[2]}"
        return roc_date_str
    except:
        return roc_date_str

def clean_numeric(value):
    """處理數字中的逗號與特殊符號，以便存入資料庫數值欄位"""
    return value.replace(',', '').replace('--', '0').strip()

# 1. 建立與 SQL Server 的連線
try:
    conn = pymssql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 建立資料表（如果不存在）
    create_table_query = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{TABLE_NAME}' AND xtype='U')
    CREATE TABLE {TABLE_NAME} (
        日期 DATETIME2,
        成交股數 VARCHAR(50),
        成交金額 NVARCHAR(50),
        開盤價 NVARCHAR(50),
        最高價 NVARCHAR(50),
        最低價 NVARCHAR(50),
        收盤價 NVARCHAR(50),
        漲跌價差 FLOAT,
        成交筆數 VARCHAR(50),
        註記 NVARCHAR(50)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("資料庫連線成功，資料表檢查完成。")

except Exception as db_e:
    print(f"資料庫初始化失敗: {db_e}")
    exit()

# 2. 啟動瀏覽器爬取資料
stock_no = "2330"
啟動 = webdriver.Chrome()
啟動.get("https://www.twse.com.tw/zh/trading/historical/stock-day.html")
等待 = WebDriverWait(啟動, 10)

try:
    等待.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
    股票代碼 = 啟動.find_element(By.NAME, "stockNo")
    股票代碼.clear()
    股票代碼.send_keys(stock_no)
    time.sleep(random.uniform(2, 4))

    for 年 in range(2020, 2027):
        for 月 in range(1, 13):
            # 限制抓取時間至 2026/03
            if 年 == 2026 and 月 > 3:
                break

            選擇年份 = Select(啟動.find_element(By.NAME, "yy"))
            選擇月份 = Select(啟動.find_element(By.NAME, "mm"))
            選擇年份.select_by_value(str(年))
            選擇月份.select_by_value(str(月))

            查詢按鈕 = 啟動.find_element(By.CSS_SELECTOR, ".submit button.search")
            查詢按鈕.click()
            
            # 等待表格或無資料提示出現
            time.sleep(random.uniform(4, 7)) 
            print(f"正在抓取 {年}/{月:02d}...")

            try:
                列 = 啟動.find_elements(By.CSS_SELECTOR, "div.rwd-table table tbody tr")

                if len(列) > 0 and "查詢無資料" not in 列[0].text:
                    data_to_insert = []
                    
                    for row in 列:
                        欄位 = row.find_elements(By.TAG_NAME, "td")
                        if 欄位:
                            raw = [c.text.strip() for c in 欄位]
                            # 格式化資料以符合 SQL 欄位
                            formatted_row = (
                                convert_to_ad_date(raw[0]),  # 日期
                                clean_numeric(raw[1]),       # 成交股數
                                clean_numeric(raw[2]),       # 成交金額
                                clean_numeric(raw[3]),       # 開盤價
                                clean_numeric(raw[4]),       # 最高價
                                clean_numeric(raw[5]),       # 最低價
                                clean_numeric(raw[6]),       # 收盤價
                                clean_numeric(raw[7]),       # 漲跌價差
                                clean_numeric(raw[8]),       # 成交筆數
                                stock_no                     # 股票代碼
                            )
                            data_to_insert.append(formatted_row)

                    # 執行批次寫入 SQL Server
                    insert_query = f"INSERT INTO {TABLE_NAME} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(insert_query, data_to_insert)
                    conn.commit()
                    print(f"成功存入 {len(data_to_insert)} 筆資料。")
                else:
                    print("跳過：無交易資料")

            except Exception as e:
                print(f"解析或寫入出錯: {e}")

    print("--- 所有任務執行完畢 ---")

except Exception as e:
    print(f"程式運行發生錯誤: {e}")

finally:
    cursor.close()
    conn.close()
    啟動.quit()