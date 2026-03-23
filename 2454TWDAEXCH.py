import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def convert_to_ad_date(roc_date_str):
    try:
        parts = roc_date_str.split('/')
        if len(parts) == 3:
            ad_year = int(parts[0]) + 1911
            return f"{ad_year}/{parts[1]}/{parts[2]}"
        return roc_date_str
    except:
        return roc_date_str

啟動 = webdriver.Chrome()
啟動.get("https://www.twse.com.tw/zh/trading/historical/stock-day.html")

等待 = WebDriverWait(啟動, 10)

try:

    等待.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
    股票代碼 = 啟動.find_element(By.NAME, "stockNo")
    股票代碼.clear()
    股票代碼.send_keys("2454")
    隨機暫停A = random.uniform(3, 5)
    time.sleep( 隨機暫停A )

    with open('股票_2454.csv', 'w', newline='', encoding='utf-8-sig') as f:
        寫入 = csv.writer(f)
        header_written = False

        for 年 in range(2010, 2027):
            for 月 in range(1, 13):
                if 年 == 2026 and 月 > 3:
                    break

                選擇年份 = Select(啟動.find_element(By.NAME, "yy"))
                選擇月份 = Select(啟動.find_element(By.NAME, "mm"))

                選擇年份.select_by_value(str(年))
                選擇月份.select_by_value(str(月))

                查詢按鈕= 啟動.find_element(By.CSS_SELECTOR, ".submit button.search")
                查詢按鈕.click()
                等待.until(EC.presence_of_element_located((By.CLASS_NAME, "rwd-table")))

                隨機暫停B = random.uniform(3, 8)
                print(f"正在抓取 {年}/{月:02d}")
                time.sleep(隨機暫停B)

                try:
                    列 = 啟動.find_elements(By.CSS_SELECTOR, "div.rwd-table table tbody tr")

                    if len(列) > 0 and "查詢無資料" not in 列[0].text:

                        if not header_written:
                            headers = 啟動.find_elements(By.CSS_SELECTOR, "div.rwd-table table thead tr th")
                            寫入.writerow([h.text.strip() for h in headers])
                            header_written = True

                        for row in 列:
                            欄位 = row.find_elements(By.TAG_NAME, "td")
                            if 欄位:
                                原始資料 = [c.text.strip() for c in 欄位]
                                原始資料[0] = convert_to_ad_date(原始資料[0])
                                寫入.writerow(原始資料)

                        print("完成抓取")
                    else:
                        print("跳過：無交易資料")

                except Exception as 資料表錯誤:
                    print(f"{資料表錯誤}")

    print("資料抓取完成!確認股票_2454.csv 檔案。")

except Exception as e:
    print(f"程式運行發生錯誤: {e}")

finally:
    啟動.quit()