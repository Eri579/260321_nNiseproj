import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def convert_multiple_excel_to_utf8_csv():
    # 初始化 tkinter 並隱藏主視窗
    root = tk.Tk()
    root.withdraw()
    
    # 強制視窗置頂（避免視窗縮小到工作列沒看到）
    root.attributes("-topmost", True)

    # 1. 操作視窗：選取多個原始 Excel 檔案
    file_paths = filedialog.askopenfilenames(
        parent=root,
        title="1. 請選擇要轉換的 Excel 檔案 (可按住 Ctrl 或 Shift 多選)",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    # 如果沒選檔案就結束
    if not file_paths:
        return

    # 2. 操作視窗：選取儲存路徑 (存取資料夾)
    save_directory = filedialog.askdirectory(
        parent=root,
        title="2. 請選擇轉換後 CSV 的儲存位置"
    )
    
    if not save_directory:
        return

    success_count = 0
    error_files = []

    # 3. 處理逻辑
    for file_path in file_paths:
        try:
            # 取得原始檔名並組合出新的存檔路徑
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            save_path = os.path.join(save_directory, f"{base_name}.csv")

            # 讀取 Excel
            df = pd.read_excel(file_path)

            # 轉換為 UTF-8-SIG CSV (台灣/中文使用者最推薦的格式)
            df.to_csv(save_path, index=False, encoding='utf-8-sig')
            
            success_count += 1

        except Exception as e:
            error_files.append(f"{os.path.basename(file_path)}: {str(e)}")

    # 4. 顯示處理結果
    if error_files:
        error_msg = "\n".join(error_files)
        messagebox.showwarning("處理完成 (部分失敗)", f"成功：{success_count}\n失敗：{len(error_files)}\n\n錯誤清單：\n{error_msg}")
    else:
        messagebox.showinfo("成功", f"恭喜！所有檔案 ({success_count}個) 已成功轉為 CSV。\n\n儲存路徑：{save_directory}")

    # 關閉視窗資源
    root.destroy()

if __name__ == "__main__":
    convert_multiple_excel_to_utf8_csv()