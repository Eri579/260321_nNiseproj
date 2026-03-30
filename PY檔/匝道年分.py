import pandas as pd
import re

# 1. 讀取你上一步產出的檔案
input_file = '合併後的交通量總表_含縣市維度.csv'
output_file = '合併後的交通量總表_標準化時間維度.csv'

try:
    df = pd.read_csv(input_file, encoding='utf-8-sig')

    # 2. 轉換函數：提取數字並加 1911
    def convert_to_ad(year_str):
        if pd.isna(year_str):
            return None
        # 使用正規表達式提取數字部分 (例如從 "107年" 提取出 "107")
        year_num = re.findall(r'\d+', str(year_str))
        if year_num:
            return int(year_num[0]) + 1911
        return None

    # 3. 執行轉換
    # 假設原始欄位叫 '年度標籤'，我們將其改寫或新增一欄 '年份'
    df['年份'] = df['年度標籤'].apply(convert_to_ad)

    # 4. (選配) 建議移除舊的 '年度標籤' 欄位，保持資料整潔
    # df = df.drop(columns=['年度標籤'])

    # 5. 再次調整欄位順序，將 '年份' 放到最前面
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('年份')))
    df = df[cols]

    # 6. 匯出
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ 轉換成功！新檔案已儲存為: {output_file}")
    print(df[['年份', '年度標籤', '縣市', '交流道']].head())

except Exception as e:
    print(f"❌ 發生錯誤: {e}")