import pandas as pd
import io
import requests

def fetch_taiwan_area_data():
    # 內政部：112年各鄉鎮市區土地面積 (CSV 下載連結)
    # 備註：若連結失效，可至 data.gov.tw 搜尋「各鄉鎮市區土地面積」更新 URL
    url = "https://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?DATA=F957193F-42E3-40A0-9E11-3E2A346C0A98"
    
    print("正在從政府公開平台抓取面積資料...")
    
    try:
        response = requests.get(url)
        response.encoding = 'utf-8' # 政府資料現在大多採 UTF-8
        
        # 讀取 CSV
        df = pd.read_csv(io.StringIO(response.text))
        
        # 1. 重新命名欄位 (根據該資料集原始欄位名，通常是：區域別, 年份, 土地面積)
        # 原始欄位可能長這樣：['statistic_yyy', 'site_id', 'people_total', 'area', 'population_density']
        # 注意：不同年份的欄位名可能略有變動，建議先印出 df.columns 檢查
        
        # 假設欄位順序為：[統計年, 區域別, 土地面積, 人口數...]
        # 我們只需要「區域別」和「土地面積」
        df = df[['site_id', 'area']] 
        df.columns = ['FullAddress', 'Area_Size_KM2']
        
        # 2. 資料清洗：切分縣市與行政區
        # site_id 格式通常是 "臺北市松山區"
        df['County'] = df['FullAddress'].str[:3]
        df['District'] = df['FullAddress'].str[3:]
        
        # 3. 移除「總計」列 (例如：新北市總計)
        df = df[df['District'] != ""]
        df = df[~df['District'].str.contains('總計')]
        
        # 4. 統一「臺」與「台」 (建議專案統一用「臺」)
        df['County'] = df['County'].str.replace('台', '臺')
        
        # 轉為浮點數
        df['Area_Size_KM2'] = pd.to_numeric(df['Area_Size_KM2'], errors='coerce')
        
        print(f"成功抓取 {len(df)} 筆行政區面積資料！")
        return df[['County', 'District', 'Area_Size_KM2']]

    except Exception as e:
        print(f"抓取失敗，錯誤訊息: {e}")
        return None

# 執行
area_df = fetch_taiwan_area_data()

if area_df is not None:
    # 存成 CSV 方便匯入 SQL
    area_df.to_csv('Taiwan_Area_Dim.csv', index=False, encoding='utf-8-sig')
    print("已存成 Taiwan_Area_Dim.csv")
    print(area_df.head())