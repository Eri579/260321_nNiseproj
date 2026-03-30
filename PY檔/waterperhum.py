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

            if start_index is not None:

                current_end = end_index if end_index is not None else len(df)

                for i in range(start_index, current_end):
                    city_name = str(df.iloc[i, 0]).strip()

                    usage_val = df.iloc[i, 3]
                    population_val = df.iloc[i, 4]

                    if city_name and city_name != 'nan' and not pd.isna(usage_val):
                        all_data_list.append({
                            '年份': year_str,
                            '縣市別': city_name,
                            '生活用水量(立方公尺)': usage_val,
                            '年中供水人數(人)': population_val
                        })

        except Exception as e:
            print(f"處理檔案 {filename} 時發生錯誤: {e}")

    if all_data_list:
        final_df = pd.DataFrame(all_data_list)
        save_path = filedialog.asksaveasfilename(
            title="儲存彙整結果",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if save_path:
            try:
                final_df.to_excel(save_path, index=False, sheet_name='用水量與人數明細')
                messagebox.showinfo("完成", f"已成功彙整 {len(all_data_list)} 筆資料！\n檔案儲存於：{save_path}")
            except Exception as e:
                messagebox.showerror("錯誤", f"儲存檔案時失敗：{e}")
    else:
        messagebox.showwarning("提示", "未能提取到任何有效資料，請檢查 Excel 格式是否正確。")


root = tk.Tk()
root.title("水利署資料自動彙整工具 v2.0")
root.geometry("450x300")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (450 / 2)
y = (screen_height / 2) - (300 / 2)
root.geometry(f'450x300+{int(x)}+{int(y)}')

tk.Label(root, text="Excel 資料批次抓取系統", font=("微軟正黑體", 14, "bold"), pady=15).pack()
tk.Label(root, text="目標：抓取 民國 97-114 年 縣市明細", fg="#555555").pack()

description = """
【擷取欄位說明】
1. 年份 (由檔名自動偵測)
2. 縣市別 (逐筆列出，排除總計)
3. 生活用水量 (立方公尺)
4. 年中供水人數 (人)
"""
tk.Label(root, text=description, justify="left", pady=10, fg="blue", font=("微軟正黑體", 9)).pack()

btn = tk.Button(root, text="選擇資料夾並執行", command=process_water_excel,
                bg="#28a745", fg="white", font=("微軟正黑體", 10, "bold"),
                padx=25, pady=10, cursor="hand2")
btn.pack(pady=10)

root.mainloop()