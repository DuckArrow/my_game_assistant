import streamlit as st
import os
# web_scraper.py は現在使用しませんが、ファイルはプロジェクト内に存在します。
# したがって、ここではインポートしません。
from gemini_assistant import initialize_gemini_model, ask_gemini

# ページ設定
st.set_page_config(
    page_title="ゲーム攻略アシスタント",
    page_icon="🎮",
    layout="centered"
)

# タイトル
st.title("🎮 ゲーム攻略アシスタント")
st.write("Webサイトの情報とGemini AIを使って、あなたの質問に答えます。")

# APIキーの取得 (環境変数からのみ)
gemini_api_key = os.getenv("GEMINI_API_KEY")

# セッション状態の初期化
# Streamlitアプリが再実行されても状態を保持するために使用します。
if "messages" not in st.session_state:
    st.session_state.messages = [] # 会話履歴を格納
if "game_name" not in st.session_state:
    st.session_state.game_name = "" # 現在のゲーム名
if "url" not in st.session_state:
    st.session_state.url = "" # 参照URL
    
# Geminiモデルの初期化 (パフォーマンスのためにキャッシュ)
# @st.cache_resource デコレータは、関数が同じ引数で呼び出された場合、
# その結果をキャッシュし、アプリの再実行時に再計算しないようにします。
@st.cache_resource
def get_gemini_model(_api_key):
    """
    Geminiモデルを初期化し、キャッシュします。
    """
    if not _api_key:
        return None
    try:
        model = initialize_gemini_model(_api_key)
        return model
    except Exception as e:
        # モデル初期化のエラーをStreamlit UIに表示
        st.error(f"Geminiモデルの初期化中にエラーが発生しました。APIキーが正しいか、またはモデル名が利用可能か確認してください: {e}")
        return None

# モデルの初期化を試みる
gemini_model = get_gemini_model(gemini_api_key)

# APIキーの存在チェック
if not gemini_api_key:
    st.error("エラー: GEMINI_API_KEY環境変数が設定されていません。")
    st.warning("APIキーを設定してから再度実行してください。")
    st.warning("例: Linux/macOS/WSL: `export GEMINI_API_KEY='YOUR_API_KEY_HERE'`")
    st.stop() # APIキーがない場合はアプリの実行を停止

# モデル初期化の失敗チェック
if gemini_model is None:
    st.error("Geminiモデルの初期化に失敗しました。APIキーが正しいか確認してください。")
    st.stop() # モデル初期化に失敗した場合はアプリの実行を停止

# セッションリセットボタン (サイドバーに配置)
if st.sidebar.button("セッションをリセットして最初から始める"):
    st.session_state.messages = [] # 会話履歴をクリア
    st.session_state.game_name = "" # ゲーム名をクリア
    st.session_state.url = "" # URLをクリア
    st.rerun() # アプリを再実行し、初期状態に戻す

# メインアプリケーションロジック

# セッション開始フェーズ: ゲーム名が設定されていない場合
if not st.session_state.game_name:
    st.subheader("セッション開始")
    # 攻略したいゲーム名を入力 (必須)
    game_name_input = st.text_input("攻略したいゲーム名を入力してください (必須):", "", key="initial_game_name")
    # 参考にしたいURLを入力 (任意)
    url_input = st.text_input("参考にしたい攻略サイトや情報のURLを入力してください (任意):", "", key="initial_url")

    # セッション開始ボタン
    if st.button("アシスタントとのセッションを開始する"):
        # ゲーム名が入力されているかを確認
        if not game_name_input:
            st.warning("ゲーム名を入力してください。")
        else:
            with st.spinner("アシスタントとのセッションを準備中..."):
                st.session_state.game_name = game_name_input # ゲーム名をセッション状態に保存
                st.session_state.url = url_input # URLをセッション状態に保存 (空でも可)

                # 初回のアシスタントメッセージを構築し、会話履歴に追加
                initial_assistant_message = f"**{st.session_state.game_name}** の攻略アシスタントを開始します。\n\n"
                if st.session_state.url:
                    initial_assistant_message += f"参照URLとして **{st.session_state.url}** を受け取りました。この情報を優先して回答を試みます。\n"
                else:
                    initial_assistant_message += "参照URLはありませんが、**Web検索（Grounding機能）** を使って質問に答えます。\n"
                
                initial_assistant_message += "何か質問はありますか？"
                
                st.session_state.messages.append({"role": "assistant", "content": initial_assistant_message})
                st.rerun() # ページを再実行し、会話フェーズへ移行

# 会話フェーズ: ゲーム名が設定されている場合
else:
    st.subheader(f"🎮 {st.session_state.game_name} の攻略アシスタント")
    if st.session_state.url:
        st.write(f"（参照URL: {st.session_state.url}）")
    else:
        st.write("（Webサイトの参照なし、Gemini AIのWeb検索を利用）")

    # 既存のメッセージ履歴を表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザーからの新しい質問を受け付けるチャット入力欄
    if prompt := st.chat_input("質問を入力してください..."):
        # ユーザーの質問を履歴に追加し、表示
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("考え中..."):
                # Gemini APIに渡すための会話履歴を構築
                # Gemini APIは `{"role": "role_name", "parts": ["content_text"]}` の形式を期待します。
                conversation_for_gemini = []
                
                # Streamlitのセッション履歴をGemini APIが期待する形式に変換
                # 最初のユーザーのターンにのみ、ゲーム名とURL情報を付加した特別なプロンプトを生成します。
                for i, msg in enumerate(st.session_state.messages):
                    if i == 0 and msg["role"] == "assistant":
                        # アシスタントの初期ウェルカムメッセージ（UI表示用）はGeminiには渡しません。
                        continue 
                    
                    # ユーザーからの最初の具体的な質問（履歴の2番目のメッセージ、つまり最初の'user'ロール）
                    if i == 1 and msg["role"] == "user": 
                         if st.session_state.url:
                             # URLがある場合はURL参照を優先する指示をプロンプトに含めます。
                             formatted_content = f"""
                            あなたはゲーム攻略アシスタントです。ユーザーの質問に対し、**提供されたURL（{st.session_state.url}）の情報を最優先に参照し、そのURLから回答が得られない場合や、より補足情報が必要な場合のみWeb検索（Grounding機能）を活用して**、最も適切で役立つ攻略情報を提供してください。
                            回答は日本のゲームプレイヤー向けに、分かりやすく、整理された自然な日本語で提供してください。

                            ---
                            **ゲーム名:** {st.session_state.game_name}
                            ---
                            ユーザーからの質問: {msg["content"]}
                            """
                         else:
                             # URLがない場合はWeb検索のみの指示をプロンプトに含めます。
                             formatted_content = f"""
                            あなたはゲーム攻略アシスタントです。ユーザーの質問に対し、**Web検索（Grounding機能）を活用して**、最も適切で役立つ攻略情報を提供してください。
                            回答は日本のゲームプレイヤー向けに、分かりやすく、整理された自然な日本語で提供してください。

                            ---
                            **ゲーム名:** {st.session_state.game_name}
                            ---
                            ユーザーからの質問: {msg["content"]}
                            """
                         conversation_for_gemini.append({"role": msg["role"], "parts": [formatted_content]})
                    else:
                        # それ以外のメッセージは、コンテンツをそのままpartsリストに入れて追加します。
                        conversation_for_gemini.append({"role": msg["role"], "parts": [msg["content"]]})

                # Gemini AIに問い合わせを行う
                gemini_response = ask_gemini(gemini_model, conversation_for_gemini)

                if gemini_response:
                    st.markdown(gemini_response) # Geminiの回答をUIに表示
                    st.session_state.messages.append({"role": "assistant", "content": gemini_response}) # 回答を履歴に追加
                else:
                    st.error("Gemini AIからの回答取得に失敗しました。")

