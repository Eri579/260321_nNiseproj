import pandas as pd

# 1. 讀取資料 (請確保檔名正確)
df = pd.read_csv('市區汽車客運路線與車輛數.csv', encoding='utf-8-sig')

def melt_and_clean_transport_data(df):
    # 2. 欄位名稱處理：假設第一欄是時間(如 '105年01月')，其餘是縣市
    time_col = df.columns[0]
    city_cols = df.columns[1:]
    
    # 3. 寬轉長 (Unpivot)：將縣市欄位轉化為「縣市」與「數值」兩欄
    df_long = df.melt(
        id_vars=[time_col], 
        value_vars=city_cols, 
        var_name='縣市', 
        value_name='營業行車次數'
    )
    
    # 4. 刪除「總計」縣市 (避免與各縣市加總重複)
    df_long = df_long[df_long['縣市'] != '總計']
    
    # 5. 分割年、月
    # 格式範例：'105年01月' -> Year: 2016, Month: 01
    # 格式範例：'105年'    -> Year: 2016, Month: NaN
    df_long['Year'] = df_long[time_col].str.extract(r'(\d+)年')[0].astype(int) + 1911
    df_long['Month'] = df_long[time_col].str.extract(r'年(\d+)月')[0] # 提取月份數字
    
    # 6. 清除年度總計列：根據你的提議，月份欄位為 NaN (空值) 的即為年度總計
    df_result = df_long.dropna(subset=['Month']).copy()
    
    # 7. 整理最後格式
    df_result['Month'] = df_result['Month'].astype(int)
    final_cols = ['Year', 'Month', '縣市', '營業行車次數']
    df_result = df_result[final_cols].sort_values(['Year', 'Month', '縣市'])
    
    return df_result

# 執行轉換
df_transport_final = melt_and_clean_transport_data(df)

# 8. 匯出成果
df_transport_final.to_csv('Transport_Cleaned.csv', index=False, encoding='utf-8-sig')
print("✅ 運輸數據轉換完成！")
print(df_transport_final.head())