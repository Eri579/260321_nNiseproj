這是一個為您的 GitHub 專案準備的 `README.md` 範本。您可以直接複製以下內容並根據需要進行微調。

---

# 股票爬蟲專案：蟲蟲危機 🐛

本專案包含兩支 Python 爬蟲程式，專門用於抓取台積電（TSM / 2330.TW）的歷史股價資料。

## 📂 專案內容

### 1. 爬蟲程式 (`.py`)
* **兩隻爬蟲.py**：核心爬蟲腳本，負責自動化抓取與處理數據。

### 2. 數據資料 (`.csv`)
* **TSM_2330TW_Stock_Data.csv**：包含台積電從 **2010 年至 2026 年 3 月 20 日** 的完整股票資料。
    * 資料範圍：2010-01-01 ~ 2026-03-20
    * 包含欄位：日期、開盤價、最高價、最低價、收盤價、成交量等。

## 🛠 使用技術與工具
* **Python**：主要開發語言。
* **Selenium / Beautiful Soup**：網頁自動化與解析。
* **WebScraper (Instant Data Scraper)**：輔助抓取工具。

## 📖 學習資源與參考
如果您在操作網頁爬蟲時遇到問題，推薦參考 **PAPAYA 電腦教室** 的教學影片。老師詳細解說了如何使用免寫程式的工具（如 Instant Data Scraper）輕鬆上手：

* **教學連結**：[原來抓網頁資料已經變得那麼簡單了？ (PAPAYA 老師)](https://www.youtube.com/watch?v=0xzTzw6GQiw)
* **影片重點**：
    * 如何安裝並使用瀏覽器擴充功能 `Instant Data Scraper` [[00:11](http://www.youtube.com/watch?v=0xzTzw6GQiw&t=11)]。
    * 自動分頁抓取大量資料的方法 [[01:07](http://www.youtube.com/watch?v=0xzTzw6GQiw&t=67)]。
    * 將抓取的資料匯出為 Excel 或 CSV 格式 [[01:39](http://www.youtube.com/watch?v=0xzTzw6GQiw&t=99)]。
    * 進階工具 `Octoparse` 的使用建議與資料清理技巧 [[02:43](http://www.youtube.com/watch?v=0xzTzw6GQiw&t=163)]。

---

## 🚀 如何開始
1. 確保已安裝 Python 3.x。
2. 安裝必要套件：`pip install selenium pandas`。
3. 執行程式：`python 兩隻爬蟲.py`。

---

### 💡 提示
如果您有任何問題，除了查看代碼註解外，觀看上述影片能幫您更快理解網頁結構與爬取邏輯！


http://googleusercontent.com/youtube_content/0
