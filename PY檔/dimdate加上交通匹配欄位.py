import pandas as pd

# 1. 載入 Excel 檔案 (請確保已安裝 openpyxl: pip install openpyxl)
file_path = 'DimDate_2000-2045.xlsx'
# 如果你的活頁簿有多個分頁，可以用 sheet_name='工作表1' 指定
df_time = pd.read_excel(file_path)

# 2. 核心對齊邏輯定義
# 這裡對應高公局數據的分類
mapping_rules = {
    '週二': '週2-4',
    '週三': '週2-4',
    '週四': '週2-4',
    '週六': '週六',
    '週日': '週日'
}

# 3. 執行欄位轉換
# 我們先處理「星期」欄位，確保沒有多餘的空白
df_time['星期'] = df_time['星期'].str.strip()

# 建立「Traffic_Day_Type」欄位
df_time['Traffic_Day_Type'] = df_time['星期'].map(mapping_rules)

# 4. 處理特殊情況：週一與週五
# 根據我們先前的分析，週一與週五不屬於這三類，我們明確標註為 '不適用' 或 NaN
# 這樣在後續 JOIN 時，這些日子就不會帶入錯誤的平均值
df_time['Traffic_Day_Type'] = df_time['Traffic_Day_Type'].fillna('非參考日')

# 5. (進階) 排除國定假日
# 如果「是否為假日」欄位顯示為「是」，則不應對齊到常態參考值
if '是否為假日' in df_time.columns:
    df_time.loc[df_time['是否為假日'] == '是', 'Traffic_Day_Type'] = '特殊假日'

# 6. 儲存結果 (建議存成 CSV 方便匯入資料庫，或存回 Excel)
output_path = 'DimDate_2000-2045_已加工.csv'
df_time.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"處理完成！已產出對齊欄位。")
print(df_time[['日期', '星期', 'Traffic_Day_Type']].head(10))