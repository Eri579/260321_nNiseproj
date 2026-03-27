import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox


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

        target_regions = ['北部區域', '中部區域', '南部區域', '東部區域']

        for sheet_name, df in all_sheets.items():

            data_subset = df.iloc[4:].copy()
            data_subset = data_subset.iloc[:, [0, 1, 6, 7, 8, 9, 12]]

            data_subset.columns = [
                '名稱', '土地面積(平方公里)', '人口數',
                '占總人口比率(%)', '男性人口數', '女性人口數', '人口密度(人/平方公里)'
            ]

            data_subset['名稱'] = data_subset['名稱'].astype(str).str.strip()

            mask = (
                    data_subset['名稱'].str.contains('市|縣') |
                    data_subset['名稱'].str.contains('|'.join(target_regions))
            )

            final_subset = data_subset[mask].copy()
            final_subset = final_subset[~final_subset['名稱'].str.contains('小計|說明|總計|註')]

            final_subset.insert(0, '時間', sheet_name)

            all_data.append(final_subset)

        if not all_data:
            messagebox.showwarning("警告", "未從檔案中抓取到任何有效資料。")
            return

        final_df = pd.concat(all_data, ignore_index=True)

        output_path = filedialog.asksaveasfilename(
            title="儲存整理後的檔案",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="縣市與區域人口資料彙整.xlsx"
        )

        if output_path:
            final_df.to_excel(output_path, index=False)
            messagebox.showinfo("成功", f"資料整理完成！\n已包含縣市及四大區域數據。\n檔案儲存於：{output_path}")

    except Exception as e:
        messagebox.showerror("錯誤", f"處理過程中發生問題：\n{str(e)}")


if __name__ == "__main__":
    process_excel()