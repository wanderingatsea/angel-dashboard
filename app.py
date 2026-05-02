import streamlit as st
import pandas as pd
import plotly.express as px

# 設定網頁標題與佈局
st.set_page_config(page_title="天使投資公司決策儀表板", page_icon="👼", layout="wide")

st.title("👼 天使投資公司 - 戰情室儀表板")

st.sidebar.header("🛡️ 天使守則 (核心風控)")
st.sidebar.info(
    "1. **波段生命線**：嚴守 20MA (月線) 支撐\n"
    "2. **紀律止損**：跌破月線 2% 啟動警示\n"
    "3. **絕對停損**：單一持股虧損達 -7%\n"
    "4. **資金管理**：集中火力於 1-2 支標的"
)

SHEET_ID = "1YIbuxAJXMHFwFFjWZvnudiPDlA7tagVBUNAP2yVPYpo"
# 改用最穩定的 CSV 匯出網址直接讀取公開資料
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        return None

df = load_data()

if df is not None and not df.empty:
    st.markdown("### 📊 監控清單與建議")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 📈 視覺化數據分析")
    
    col1, col2 = st.columns(2)
    with col1:
        if '股票名稱' in df.columns and '融資餘額' in df.columns:
            df['融資餘額(張)'] = df['融資餘額'].astype(str).str.replace(',', '').astype(float)
            fig_margin = px.bar(df, x='股票名稱', y='融資餘額(張)', color='股票名稱', title="散戶籌碼：融資餘額監控")
            st.plotly_chart(fig_margin, use_container_width=True)

    with col2:
        if '股票名稱' in df.columns and '券資比' in df.columns:
            df['券資比(%)'] = df['券資比'].astype(str).str.replace('%', '').astype(float)
            fig_ratio = px.pie(df, names='股票名稱', values='券資比(%)', title="軋空潛力：券資比分佈", hole=0.4)
            fig_ratio.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_ratio, use_container_width=True)
else:
    st.error("讀取 Google Sheet 失敗。請確認試算表權限已設為「知道連結的人均可檢視」。")

