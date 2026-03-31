import pandas as pd

# 1. 載入原始資料
file_path = '合併後的交通量總表_含縣市與年.csv'
df = pd.read_csv(file_path)

# 2. 定義固定不動的欄位 (ID variables)
# 根據你的圖片，包含：年, 年度標籤, 路線方向, 路段, 交流道, 縣市, 進出口
id_cols = ['年', '年度標籤', '路線方向', '路段', '交流道', '縣市', '進出口']

# 3. 執行逆樞紐 (Unpivot)
# value_vars 指定要被拆解的欄位
# var_name 是拆解後類別的名稱，value_name 是數值的名稱
df_unpivoted = pd.melt(
    df, 
    id_vars=id_cols, 
    value_vars=['週六', '週日', '週2-4'],
    var_name='Day_Type', 
    value_name='Traffic_Volume'
)

# 4. 排序與匯出
# 排序能讓資料更具備可讀性，方便後續檢查
df_unpivoted = df_unpivoted.sort_values(by=['年', '交流道', 'Day_Type'])

# 匯出新檔案
output_path = '交通量總表_Unpivoted.csv'
df_unpivoted.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"逆樞紐完成！新檔案已儲存至: {output_path}")
print(df_unpivoted.head())