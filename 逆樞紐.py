import pandas as pd
import re
import os

# 1. 參數設定
input_file = "===10701-11502產業每月營業額_思.csv"
output_file = "Cleaned_Retail_Revenue_Final.csv"

if not os.path.exists(input_file):
    print(f"找不到檔案：{input_file}")
else:
    df = pd.read_csv(input_file, encoding="utf-8-sig")

    def process_date_logic(row):
        try:
            y_match = re.search(r'\d+', str(row['年']))
            m_match = re.search(r'\d+', str(row['月']))
            if y_match and m_match:
                ad_year = int(y_match.group()) + 1911
                month_str = m_match.group().zfill(2) 
                std_date = f"{ad_year}-{month_str}-01"
                return pd.Series([ad_year, month_str, std_date])
            return pd.Series([None, None, None])
        except:
            return pd.Series([None, None, None])

    df[['Year', 'Month', 'Standard_Date']] = df.apply(process_date_logic, axis=1)
    df_clean = df.dropna(subset=['Standard_Date']).copy()

    # 3. 執行逆樞紐 (Melt)
    id_vars = ['Standard_Date', 'Year', 'Month']
    exclude_cols = ['年', '月', 'Standard_Date', 'Year', 'Month']
    value_vars = [col for col in df_clean.columns if col not in exclude_cols]

    df_long = df_clean.melt(
        id_vars=id_vars, 
        value_vars=value_vars, 
        var_name='Industry_Category', 
        value_name='Revenue'
    )

    # 4. 金額轉換與清洗
    df_long['Revenue'] = pd.to_numeric(
        df_long['Revenue'].astype(str).str.replace(',', '').replace('-', '0'), 
        errors='coerce'
    ).fillna(0)

    # --- 關鍵修正：刪除每個月第一列的空白行 ---
    # 邏輯：如果 Industry_Category 為空，或 Revenue 為 0，則視為無效行
    # 我們使用 .strip() 確保不會被隱形成空格騙過
    df_long['Industry_Category'] = df_long['Industry_Category'].astype(str).str.strip()
    
    # 執行過濾：保留「營業額大於 0」且「產業類別不是空白/nan」的資料
    df_long = df_long[
        (df_long['Revenue'] > 0) & 
        (df_long['Industry_Category'] != '') & 
        (df_long['Industry_Category'] != 'nan')
    ]
    # ---------------------------------------

    df_long = df_long.sort_values(['Standard_Date', 'Industry_Category'])
    df_long = df_long[['Standard_Date', 'Year', 'Month', 'Industry_Category', 'Revenue']]

    df_long.to_csv(output_file, index=False, encoding="utf-8-sig")
    
    print("-" * 30)
    print(f"清洗成功！已自動剔除每個月分的空白間隔行。")
    print(f"剩餘有效資料筆數: {len(df_long)}")
    print(df_long.head(15)) # 印出前15筆確認 7 月的空白行是否消失