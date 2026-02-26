import streamlit as st
import yfinance as yf
import google.generativeai as genai
import plotly.graph_objects as go

# --- 設定の読み込み ---
try:
    if "gemini" in st.secrets:
        api_key = st.secrets["gemini"]["api_key"]
        # APIキーの前後にある可能性のある「隠れたスペース」を削除して設定
        genai.configure(api_key=api_key.strip())
    else:
        st.error("Secretsに 'api_key' が見つかりません。")
except Exception as e:
    st.error(f"初期設定エラー: {e}")

st.title("🤖 投資分析アプリ（疎通テスト版）")

if st.button('AI接続テスト開始'):
    with st.spinner('通信テスト中...'):
        # 検証：3つの異なる名前で順番に接続を試みます
        test_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        success = False
        
        for m_name in test_models:
            try:
                model = genai.GenerativeModel(m_name)
                response = model.generate_content("こんにちは、接続テストです。短く返信してください。")
                st.success(f"成功！ モデル名: {m_name}")
                st.write(f"AIからの返信: {response.text}")
                success = True
                break # 1つでも成功すれば終了
            except Exception as e:
                st.write(f"× {m_name} は接続不可")
        
        if not success:
            st.error("すべてのモデル名で接続に失敗しました。")
            st.info("原因の可能性: APIキーがまだ有効化されていないか、支払情報の登録（無料枠でも必要な場合があります）に関する制限かもしれません。")

st.markdown("---")
st.caption("2026年2月27日 検証実行中")
