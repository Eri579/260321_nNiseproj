import streamlit as st
import pandas as pd
import PI as px
from sklearn.datasets import load_iris

# --- 頁面設定 ---
st.set_page_config(page_title="鳶尾花數據分析專題", layout="wide")

# --- 1. 標題與側邊欄 ---
st.title("🌸 鳶尾花 (Iris) 資料分析互動儀表板")
st.sidebar.header("篩選條件")

# --- 2. 資料載入 ---
@st.cache_data # 快取機制，避免重複讀取
def load_data():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = [iris.target_names[i] for i in iris.target]
    return df

df = load_data()

# --- 3. 側邊欄互動元件 ---
species_choice = st.sidebar.multiselect(
    "選擇品種:", 
    options=df["species"].unique(), 
    default=df["species"].unique()
)

# 根據選擇過濾資料
filtered_df = df[df["species"].isin(species_choice)]

# --- 4. 主要視覺化區塊 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("數據概覽")
    st.write(filtered_df.head(10))
    st.metric("當前數據筆數", len(filtered_df))

with col2:
    st.subheader("特徵分佈散佈圖")
    fig = px.scatter(
        filtered_df, 
        x="sepal length (cm)", 
        y="sepal width (cm)", 
        color="species",
        title="花萼長度 vs 寬度"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 5. 數據結論 ---
st.divider()
st.markdown("### 📝 分析結論")
st.info("透過散佈圖可以觀察到，Setosa 品種在花萼尺寸上有明顯的區隔。")