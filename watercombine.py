import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re


def process_water_excel():

    folder_path = filedialog.askdirectory(title="請選擇包含 97-114 年 Excel 檔案的資料夾")
    if not folder_path:
        return

    all_data_list = []

    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')])

    if not files:
        messagebox.showwarning("提示", "該資料夾內沒有找到 Excel 檔案。")
        return

    for filename in files:
        try:

            year_match = re.search(r'(\d{2,3})', filename)
            year_str = f"民國{year_match.group(1)}年" if year_match else filename

            file_full_path = os.path.join(folder_path, filename)

            df = pd.read_excel(file_full_path, header=None)

            start_index = None
            end_index = None

            for idx, row_value in enumerate(df.iloc[:, 0]):
                val_str = str(row_value).strip()
                if "縣市別" in val_str:
                    start_index = idx + 1
                elif "總計" in val_str:
                    end_index = idx
                    break

            if start_index is not None:
                current_end = end_index if end_index is not None else len(df)

                for i in range(start_index, current_end):
                    city_name = str(df.iloc[i, 0]).strip()
                    usage_val = df.iloc[i, 3]

                    if city_name and city_name != 'nan' and not pd.isna(usage_val):
                        all_data_list.append({
                            '年份': year_str,
                            '縣市別': city_name,
                            '生活用水量(立方公尺)': usage_val
                        })

        except Exception as e:
            print(f"處理檔案 {filename} 時發生錯誤: {e}")

    if all_data_list:
        final_df = pd.DataFrame(all_data_list)
        save_path = filedialog.asksaveasfilename(
            title="儲存逐筆彙整結果",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if save_path:
            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                final_df.to_excel(writer, index=False, sheet_name='用水量明細')

            messagebox.showinfo("完成", f"已成功彙整 {len(all_data_list)} 筆縣市明細資料！\n檔案儲存於：{save_path}")
    else:
        messagebox.showwarning("提示", "未能成功提取資料，請檢查 Excel 格式。")


root = tk.Tk()
root.title("水利署資料逐筆彙整工具")
root.geometry("450x280")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (450 / 2)
y = (screen_height / 2) - (280 / 2)
root.geometry(f'450x280+{int(x)}+{int(y)}')

tk.Label(root, text="Excel 明細資料批次抓取", font=("Arial", 14, "bold"), pady=15).pack()
tk.Label(root, text="抓取 民國 97-114 年 各縣市逐筆數據", fg="#555555").pack()

description = """
【執行說明】
1. 請準備 97-114 年的 Excel 檔案放入資料夾。
2. 程式會自動跳過『總計』列，僅保留各縣市明細。
3. 自動偵測『縣市別』欄位作為起始點。
"""
tk.Label(root, text=description, justify="left", pady=10, fg="blue").pack()

btn = tk.Button(root, text="選擇資料夾並開始匯總", command=process_water_excel,
                bg="#28a745", fg="white", font=("微軟正黑體", 10, "bold"),
                padx=20, pady=10, cursor="hand2")
btn.pack(pady=10)

root.mainloop()