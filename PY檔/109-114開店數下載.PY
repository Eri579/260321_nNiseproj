import requests
import os
import time
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl

# --- 強制自定義 SSL 上下文 (解決 Missing Subject Key Identifier) ---
class DESAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        # 建立一個不檢查憑證的 SSL Context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # 強制允許較舊或不規範的憑證
        context.set_ciphers('DEFAULT@SECLEVEL=1') 
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

# --- 設定區域 ---
save_folder = "107-114開店數exl"
start_year = 112
end_year = 114

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 建立 Session 並掛載強大的自定義適配器
session = requests.Session()
session.mount('https://', DESAdapter())

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# --- 執行下載迴圈 ---
for year in range(start_year, end_year + 1):
    for month_int in range(1, 13):
        month = str(month_int).zfill(2)
        date_str = f"{year}{month}"
        
        url = f"https://service.mof.gov.tw/public/Data/statistic/monthly/{date_str}/23090_{date_str}.xlsx"
        file_name = f"開店數統計{date_str}.xlsx"
        file_path = os.path.join(save_folder, file_name)
        
        try:
            print(f"嘗試下載 {date_str} ...", end=" ", flush=True)
            
            # 使用 session 發送請求
            response = session.get(url, headers=headers, verify=False, timeout=20)
            
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print("✅ 成功！")
            elif response.status_code == 404:
                print("❌ 檔案不存在")
            else:
                print(f"⚠️ 狀態碼：{response.status_code}")
                
        except Exception as e:
            print(f"🔥 還是失敗了，錯誤原因：{e}")
        
        time.sleep(1)

print("\n--- 任務執行完畢 ---")


# 109-11201檔案是.xls
# 11202-11412檔案是.xlsx
# 107-10812無規則

