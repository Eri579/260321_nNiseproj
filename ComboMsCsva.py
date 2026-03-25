import csv
import time
import random
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import pymssql
from selenium import webdriver
from selenium.webdriver.common.by import By
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


def clean_numeric(value):
    if not value: return "0"
    cleaned = value.replace(',', '').replace('--', '0').replace('+', '').strip()
    return cleaned


def toggle_sql_frame(*args):
    if var_sql.get():
        labelframe2.pack(padx=10, pady=10, fill="both", after=labelframe1)
    else:
        labelframe2.pack_forget()


def start_scraping():
    url = entry_url.get()
    stock_id = entry_stock.get()
    raw_filename = entry_filename.get()

    do_csv = var_csv.get()
    do_sql = var_sql.get()

    sql_host = entry_host.get()
    sql_user = entry_user.get()
    sql_pwd = entry_pwd.get()
    sql_db = entry_db.get()

    start_y = int(var_start_y.get())
    start_m = int(var_start_m.get())
    end_y = int(var_end_y.get())
    end_m = int(var_end_m.get())

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    if not (do_csv or do_sql):
        messagebox.showwarning("提示", "請至少選擇一種儲存方式（CSV 或 SQL）")
        return

    if (end_y < start_y) or (end_y == start_y and end_m < start_m):
        messagebox.showwarning("日期錯誤", "結束日期不可早於開始日期！")
        return

    if not all([url, stock_id, raw_filename]):
        messagebox.showwarning("錯誤", "抓取設定欄位皆為必填！")
        return

    if do_sql and not all([sql_host, sql_user, sql_pwd, sql_db]):
        messagebox.showwarning("錯誤", "您已開啟 SQL 模式，資料庫連線欄位皆為必填！")
        return

    csv_file = raw_filename if raw_filename.endswith('.csv') else raw_filename + ".csv"
    table_name = raw_filename.replace(".csv", "")

    btn_run.config(state=tk.DISABLED, text="執行中...")
    root.update()

    conn = None
    cursor = None
    if do_sql:
        try:
            conn = pymssql.connect(
                host=sql_host,
                user=sql_user,
                password=sql_pwd,
                database=sql_db,
                charset='utf8'
            )
            cursor = conn.cursor()
            create_query = f"""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
            CREATE TABLE [{table_name}] (
                日期 DATETIME2,
                成交股數 BIGINT,
                成交金額 BIGINT,
                開盤價 FLOAT,
                最高價 FLOAT,
                最低價 FLOAT,
                收盤價 FLOAT,
                漲跌價差 FLOAT,
                成交筆數 INT,
                股票代碼 NVARCHAR(20)
            )
            """
            cursor.execute(create_query)
            conn.commit()
        except Exception as db_e:
            messagebox.showerror("資料庫錯誤", f"連線失敗: {db_e}")
            btn_run.config(state=tk.NORMAL, text="開始執行任務")
            return

    啟動 = webdriver.Chrome()

    try:
        啟動.get(url)
        等待 = WebDriverWait(啟動, 10)
        等待.until(EC.presence_of_element_located((By.NAME, "stockNo")))

        股票代碼欄 = 啟動.find_element(By.NAME, "stockNo")
        股票代碼欄.clear()
        股票代碼欄.send_keys(stock_id)

        csv_f = None
        寫入 = None
        header_written = False
        if do_csv:
            csv_f = open(csv_file, 'w', newline='', encoding='utf-8-sig')
            寫入 = csv.writer(csv_f)

        for 年 in range(start_y, end_y + 1):
            m_start = start_m if 年 == start_y else 1
            m_end = end_m if 年 == end_y else 12

            for 月 in range(m_start, m_end + 1):
                if 年 > current_year or (年 == current_year and 月 > current_month):
                    break

                Select(啟動.find_element(By.NAME, "yy")).select_by_value(str(年))
                Select(啟動.find_element(By.NAME, "mm")).select_by_value(str(月))
                啟動.find_element(By.CSS_SELECTOR, ".submit button.search").click()

                等待.until(EC.presence_of_element_located((By.CLASS_NAME, "rwd-table")))
                time.sleep(random.uniform(3, 5))

                print(f"正在抓取 {年}/{月:02d}...")

                try:
                    列 = 啟動.find_elements(By.CSS_SELECTOR, "div.rwd-table table tbody tr")
                    if len(列) > 0 and "查詢無資料" not in 列[0].text:
                        data_batch_sql = []

                        if do_csv and not header_written:
                            headers = 啟動.find_elements(By.CSS_SELECTOR, "div.rwd-table table thead tr th")
                            寫入.writerow([h.text.strip() for h in headers])
                            header_written = True

                        for row in 列:
                            欄位 = row.find_elements(By.TAG_NAME, "td")
                            if 欄位:
                                raw_data = [c.text.strip() for c in 欄位]
                                ad_date = convert_to_ad_date(raw_data[0])

                                if do_csv:
                                    csv_row = [ad_date] + raw_data[1:]
                                    寫入.writerow(csv_row)

                                if do_sql:
                                    formatted_row = (
                                        ad_date,
                                        clean_numeric(raw_data[1]),
                                        clean_numeric(raw_data[2]),
                                        clean_numeric(raw_data[3]),
                                        clean_numeric(raw_data[4]),
                                        clean_numeric(raw_data[5]),
                                        clean_numeric(raw_data[6]),
                                        clean_numeric(raw_data[7]),
                                        clean_numeric(raw_data[8]),
                                        stock_id
                                    )
                                    data_batch_sql.append(formatted_row)

                        if do_sql and data_batch_sql:
                            insert_query = f"INSERT INTO [{table_name}] VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.executemany(insert_query, data_batch_sql)
                            conn.commit()
                    else:
                        print(f"{年}/{月:02d} 無資料。")
                except Exception as e:
                    print(f"解析出錯: {e}")

            if 年 == current_year and 月 >= current_month:
                break

        messagebox.showinfo("完成", "任務執行完畢！")

    except Exception as e:
        messagebox.showerror("程式錯誤", str(e))
    finally:
        if csv_f: csv_f.close()
        if cursor: cursor.close()
        if conn: conn.close()
        啟動.quit()
        btn_run.config(state=tk.NORMAL, text="開始抓取")

root = tk.Tk()
root.title("證交所台股資料抓取API SQL/CSV")
root.geometry("650x460")

labelframe1 = tk.LabelFrame(root, text="抓取與儲存設定", padx=10, pady=10)
labelframe1.pack(padx=10, pady=10, fill="both")

tk.Label(labelframe1, text="目標網址:").grid(row=0, column=0, sticky="e")
entry_url = tk.Entry(labelframe1, width=45)
entry_url.insert(0, "https://www.twse.com.tw/zh/trading/historical/stock-day.html")
entry_url.grid(row=0, column=1, columnspan=3, pady=2)

tk.Label(labelframe1, text="股票代碼:").grid(row=1, column=0, sticky="e")
entry_stock = tk.Entry(labelframe1, width=45)
entry_stock.insert(0, "")
entry_stock.grid(row=1, column=1, columnspan=3, pady=2)

tk.Label(labelframe1, text="檔名/表名:").grid(row=2, column=0, sticky="e")
entry_filename = tk.Entry(labelframe1, width=45)
entry_filename.insert(0, "")
entry_filename.grid(row=2, column=1, columnspan=3, pady=2)

this_year = datetime.now().year
years = [str(y) for y in range(1999, this_year + 1)]
months = [str(m) for m in range(1, 13)]

tk.Label(labelframe1, text="開始日期:").grid(row=3, column=0, sticky="e")
var_start_y, var_start_m = tk.StringVar(value=""), tk.StringVar(value="")
ttk.Combobox(labelframe1, textvariable=var_start_y, values=years, width=10).grid(row=3, column=1, sticky="w")
ttk.Combobox(labelframe1, textvariable=var_start_m, values=months, width=5).grid(row=3, column=2, sticky="w")

tk.Label(labelframe1, text="結束日期:").grid(row=4, column=0, sticky="e")
var_end_y, var_end_m = tk.StringVar(value=str(this_year)), tk.StringVar(value=str(datetime.now().month))
ttk.Combobox(labelframe1, textvariable=var_end_y, values=years, width=10).grid(row=4, column=1, sticky="w")
ttk.Combobox(labelframe1, textvariable=var_end_m, values=months, width=5).grid(row=4, column=2, sticky="w")

var_csv = tk.BooleanVar(value=True)
tk.Checkbutton(labelframe1, text="儲存為 CSV", variable=var_csv).grid(row=5, column=1, sticky="w")

var_sql = tk.BooleanVar(value=False)
var_sql.trace_add("write", toggle_sql_frame)
tk.Checkbutton(labelframe1, text="上傳至SQL SERVER", variable=var_sql).grid(row=5, column=2, sticky="w")

labelframe2 = tk.LabelFrame(root, text="SQL Server 連線設定", padx=10, pady=10)
tk.Label(labelframe2, text="host:").grid(row=0, column=0, sticky="e")
entry_host = tk.Entry(labelframe2, width=30)
entry_host.insert(0, "")
entry_host.grid(row=0, column=1, pady=2, sticky="w")

tk.Label(labelframe2, text="User:").grid(row=1, column=0, sticky="e")
entry_user = tk.Entry(labelframe2, width=30)
entry_user.insert(0, "")
entry_user.grid(row=1, column=1, pady=2, sticky="w")

tk.Label(labelframe2, text="Password:").grid(row=2, column=0, sticky="e")
entry_pwd = tk.Entry(labelframe2, width=30, show="*")
entry_pwd.insert(0, "")
entry_pwd.grid(row=2, column=1, pady=2, sticky="w")

tk.Label(labelframe2, text="Database:").grid(row=3, column=0, sticky="e")
entry_db = tk.Entry(labelframe2, width=30)
entry_db.insert(0, "")
entry_db.grid(row=3, column=1, pady=2, sticky="w")

btn_run = tk.Button(root, text="開始執行任務", command=start_scraping, bg="#4CAF50", fg="white",
                    font=("微軟正黑體", 12, "bold"), height=2)
btn_run.pack(side="bottom", pady=20, fill="x", padx=50)

root.mainloop()