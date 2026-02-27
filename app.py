import streamlit as st
import google.generativeai as genai
import os

# --- 1. APIキーの設定 ---
if "gemini" in st.secrets:
    api_key = st.secrets["gemini"]["api_key"].strip()
    
    # 【最重要】環境変数という仕組みを使って、システム全体に「v1を使え」と命令します
    os.environ["GOOGLE_API_VERSION"] = "v1"
    
    # 通信方式を「REST」に固定し、ライブラリの自動選択を無効化します
    genai.configure(api_key=api_key, transport='rest')

st.set_page_config(page_title="AI投資分析", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- 2. AI分析 ---
st.header("📊 本日の市況を分析")

if st.button('分析を実行する'):
    with st.spinner('AIが回答を生成中...'):
        try:
            # モデルの取得。ここでも明示的に指定します
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            
            prompt = "あなたはプロの投資家です。2026年2月27日の株式市場について、日本とアメリカの状況を投資家視点で短く教えて。"
            
            # 通信実行
            response = model.generate_content(prompt)
            
            if response.text:
                st.success("分析が完了しました")
                st.markdown("---")
                st.write(response.text)
                st.markdown("---")
                
        except Exception as e:
            # エラーが出た場合、その時の通信先URLが見えるようにします
            st.error(f"通信エラーが発生しました。")
            st.info(f"技術詳細: {e}")
            st.write("もしエラーが続く場合、Google側が新しいキーを各サーバーにコピーするまで数分のタイムラグがあるかもしれません。")

st.markdown("---")
st.caption("2026年2月27日 運用中 (API v1 固定モード)")
