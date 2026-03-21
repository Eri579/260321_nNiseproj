import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

啟動 = webdriver.Chrome()
啟動.get("https://www.twse.com.tw/zh/trading/historical/stock-day.html")

等待 = WebDriverWait(啟動, 10)

try:

    等待.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
    股票代碼 = 啟動.find_element(By.NAME, "stockNo")
    股票代碼.clear()
    股票代碼.send_keys("2330")
    隨機暫停A = random.uniform(3, 5)
    time.sleep( 隨機暫停A )

    with open('股票_2330.csv', 'w', newline='', encoding='utf-8') as f:
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
                            欄 = row.find_elements(By.TAG_NAME, "td")
                            if 列:
                                寫入.writerow([c.text.strip() for c in 欄])

                        print("完成抓取")
                    else:
                        print("跳過：無交易資料")

                except Exception as 資料表錯誤:
                    print(f"{資料表錯誤}")

    print("資料抓取完成！確認股票_2330.csv 檔案。")

except Exception as e:
    print(f"程式運行發生錯誤: {e}")

finally:
    啟動.quit()