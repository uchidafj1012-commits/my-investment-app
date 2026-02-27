import streamlit as st
import google.generativeai as genai

# --- 1. APIキーの設定 ---
if "gemini" in st.secrets:
    api_key = st.secrets["gemini"]["api_key"].strip()
    # 余計なオプションを付けず、最も標準的な接続を行います
    genai.configure(api_key=api_key)

st.set_page_config(page_title="AI投資分析", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- 2. AI分析 ---
st.header("📊 本日の市況を分析")

if st.button('分析を実行する'):
    with st.spinner('AIが回答を生成中...'):
        try:
            # どんな状況でも認識されやすい「gemini-1.5-flash」を直接指定
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("2026年2月27日の株式市場について、日本とアメリカの状況を投資家視点で短く教えて。")
            
            st.success("分析が完了しました")
            st.write(response.text)
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.markdown("---")
st.caption("2026年2月27日 運用中")
