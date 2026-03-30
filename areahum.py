import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os


def process_excel():

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="請選擇原始 Excel 檔案",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if not file_path:
        return

    try:

        all_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
        all_data = []

        for sheet_name, df in all_sheets.items():
            data_subset = df.iloc[4:].copy()

            data_subset = data_subset.iloc[:, [0, 1, 6, 7, 8, 9, 12]]
            data_subset.columns = [
                '縣市/區域', '土地面積(平方公里)', '人口數',
                '占總人口比率(%)', '男性人口數', '女性人口數', '人口密度(人/平方公里)'
            ]

             data_subset = data_subset[data_subset['縣市/區域'].astype(str).str.contains('市|縣')]
            data_subset = data_subset[~data_subset['縣市/區域'].astype(str).str.contains('小計|區域|說明|註')]

            data_subset.insert(0, '時間', sheet_name)

            all_data.append(data_subset)

        final_df = pd.concat(all_data, ignore_index=True)

        output_path = filedialog.asksaveasfilename(
            title="儲存整理後的檔案",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="縣市人口資料彙整_2017-2026.xlsx"
        )

        if output_path:
            final_df.to_excel(output_path, index=False)
            messagebox.showinfo("成功", f"資料處理完成！\n檔案已儲存至：{output_path}")

    except Exception as e:
        messagebox.showerror("錯誤", f"處理過程中發生問題：\n{str(e)}")


if __name__ == "__main__":
    process_excel()