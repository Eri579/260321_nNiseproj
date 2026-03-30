import pandas as pd
import os

# 1. 讀取你原始的資料 (假設檔名為 raw_data.csv)
# 如果你是直接貼上資料，請參考下方的模擬資料
try:
    df = pd.read_csv('住宅買賣_住宅買賣移轉筆數_欣.csv') 
except:
    # 模擬圖片中的資料結構
    data = {
        '日期': ['098Q1', '098Q2', '098Q3', '098Q4', '099Q1'],
        '數值指標': [10.5, 11.2, 10.8, 12.1, 13.5] # 假設的數據欄位
    }
    df = pd.DataFrame(data)

def transform_and_export(df, date_col='資料期別', output_name='Transformed_Quarterly_Data.csv'):
    # 2. 格式預處理：確保為 5 位字元 (補齊如 98Q1 為 098Q1)
    df[date_col] = df[date_col].str.zfill(5)
    
    # 3. 提取民國年並轉換為西元年
    df['Year'] = df[date_col].str[:3].astype(int) + 1911
    
    # 4. 提取季度數字
    df['Quarter'] = df[date_col].str[-1].astype(int)
    
    # 5. 建立標準日期格式 (該季第一天)，這對 Power BI 或 SQL 關聯極其重要
    quarter_to_month = {1: '01-01', 2: '04-01', 3: '07-01', 4: '10-01'}
    df['StandardDate'] = pd.to_datetime(
        df['Year'].astype(str) + '-' + df['Quarter'].map(quarter_to_month)
    )
    
    # 6. 整理欄位順序：將新產生的時間維度放在最前面
    cols = ['Year', 'Quarter', 'StandardDate'] + [c for c in df.columns if c not in ['Year', 'Quarter', 'StandardDate']]
    df = df[cols]
    
    # 7. 匯出 CSV
    # encoding='utf-8-sig' 確保 Excel 打開中文不會亂碼
    df.to_csv(output_name, index=False, encoding='utf-8-sig')
    print(f"✅ 轉換完成！已匯出至: {os.path.abspath(output_name)}")
    return df

# 執行轉換
df_new = transform_and_export(df)

# 查看前幾筆確認結果
print(df_new.head())