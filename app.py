import streamlit as st
import requests
import json

# --- 1. APIキーの設定 ---
api_key = ""
if "gemini" in st.secrets:
    api_key = st.secrets["gemini"]["api_key"].strip()

st.set_page_config(page_title="AI投資分析", layout="wide")
st.title("🤖 先生専用：AI自動投資分析アプリ")

# --- 2. AI分析 ---
st.header("📊 本日の市況を分析")

if st.button('分析を実行する'):
    if not api_key:
        st.error("APIキーが設定されていません。")
    else:
        with st.spinner('AIが回答を生成中...'):
            # 【究極のシンプル化】
            # 最も古くからある名称 'gemini-pro' のみを使用し、URLも正式版(v1)に固定
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": "プロの投資家として、本日2026年2月27日の日米市況を短く教えてください。"}]
                }]
            }
            
            try:
                response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
                res_data = response.json()
                
                if response.status_code == 200:
                    answer = res_data['candidates'][0]['content']['parts'][0]['text']
                    st.success("分析が完了しました")
                    st.write(answer)
                else:
                    st.error(f"Googleサーバーが準備中です (Status: {response.status_code})")
                    st.write("このエラーはAPIキーが有効化されるまでの待機時間を示しています。")
                    st.json(res_data)
                    
            except Exception as e:
                st.error(f"通信に失敗しました: {e}")

st.markdown("---")
st.caption("2026年2月27日 運用中")
