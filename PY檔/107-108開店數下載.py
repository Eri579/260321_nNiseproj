import os
import re  # 引入正規表達式模組來抓數字
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 關閉 SSL 安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 設定目標與 Header
base_url = "https://www.mof.gov.tw"
start_url = "https://www.mof.gov.tw/singlehtml/285?cntId=0d3befe0fe9640d2a3c87bd612416683"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 修改下載函式，增加 custom_filename 參數
def download_file(url, custom_filename, folder="107-114開店數exl"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # 這裡直接組合出你要的檔名格式
    path = os.path.join(folder, f"{custom_filename}.xls")
    
    print(f"正在下載檔案: {custom_filename} (網址: {url})")
    r = requests.get(url, headers=headers, stream=True, verify=False)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"下載完成，存檔路徑: {path}")

# --- 第一層：從 A 網址找 B 網址 ---
response = requests.get(start_url, headers=headers, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

target_years = ["107年", "108年"]
b_links = []

for a_tag in soup.find_all('a', title=True):
    title_text = a_tag['title']
    if any(year in title_text for year in target_years) and "月報" in title_text:
        match = re.search(r"(\d+)年(\d+)月", title_text)
        if match:
            # 關鍵修正點zfill：確保月份有兩位數
            year = match.group(1)
            month = match.group(2).zfill(2) 
            ym_suffix = year + month
            
            b_url = urljoin(base_url, a_tag['href'])
            b_links.append((ym_suffix, b_url))
# --- 第二層：進入 B 網址抓取路徑 ---
for ym, b_url in b_links:
    res_b = requests.get(b_url, headers=headers, verify=False)
    soup_b = BeautifulSoup(res_b.text, 'html.parser')
    
    # 尋找「表3-9」且包含「xls檔」
    xls_tag = soup_b.find('a', title=lambda x: x and "表3-9" in x and "xls檔" in x)
    
    if xls_tag:
        download_path = xls_tag['href']
        full_download_url = urljoin(base_url, download_path)
        
        # 組合出最終檔名：開店數統計 + 10801
        final_name = f"開店數統計{ym}"
        download_file(full_download_url, final_name)
    else:
        print(f"在頁面中找不到 {ym} 表3-9 的 xls 下載連結")