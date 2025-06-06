import google.generativeai as genai
import os
from dotenv import load_dotenv # python-dotenv ライブラリをインポート

# .envファイルを読み込む (スクリプトの先頭で呼び出すのが一般的)
# これにより、.envファイルに定義された変数が os.environ に追加される
# ただし、すでに環境変数として設定されている場合はそちらが優先される
load_dotenv() 

def list_available_models(api_key: str):
    """
    指定されたAPIキーで利用可能なGeminiモデルのリストを出力します。
    generateContent メソッドをサポートするモデルのみを表示します。
    """
    genai.configure(api_key=api_key)
    print("\n--- 利用可能なGeminiモデルのリスト ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Name: {m.name}, Display Name: {m.display_name}, Supported Methods: {m.supported_generation_methods}")
    except Exception as e:
        print(f"モデルのリスト取得中にエラーが発生しました: {e}")
    print("--------------------------------------")


def initialize_gemini_model(api_key: str):
    """
    GeminiモデルをAPIキーで初期化します。
    環境変数 GEMINI_MODEL_NAME があればそれを使用し、なければデフォルト値を使用します。
    """
    genai.configure(api_key=api_key)
    
    # 環境変数からモデル名を読み込む。設定されていなければ 'gemini-1.5-flash' をデフォルトとする。
    # このモデルは無料枠で利用できることが多い。
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash-preview-05-20")

    try:
        model = genai.GenerativeModel(model_name=model_name)
        print(f"Geminiモデル '{model_name}' を初期化しました。") # 初期化したモデル名を表示
        return model
    except Exception as e:
        print(f"Geminiモデルの初期化中にエラーが発生しました。APIキーが正しいか、またはモデル名'{model_name}'が利用可能か確認してください: {e}")
        return None

def ask_gemini(model, conversation_history: list[dict]) -> str | None:
    """
    会話履歴全体をGeminiモデルに渡し、回答を取得します。
    """
    try:
        response = model.generate_content(
            contents=conversation_history,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        return response.text
    except Exception as e:
        print(f"Gemini API呼び出し中にエラーが発生しました: {e}")
        print("APIキーが正しいか、ネットワーク接続を確認してください。")
        print("また、プロンプトの長さがモデルの最大トークン制限を超えていないか確認してください。")
        return None

if __name__ == '__main__':
    # このブロックは、このスクリプトを直接実行した場合にのみ実行されます。
    # Streamlitアプリから呼ばれる場合は実行されません。

    # 環境変数 GEMINI_API_KEY を取得
    # load_dotenv() により、.envファイルの値もここで参照可能になる
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        print("エラー: GEMINI_API_KEY環境変数が設定されていません。")
        print("APIキーを環境変数として設定するか、.envファイルに記述してから再度実行してください。")
        exit()

    # テスト実行時のみ利用可能なモデルリストを表示 (必要であれば)
    # list_available_models(gemini_api_key)

    gemini_model = initialize_gemini_model(gemini_api_key)

    if gemini_model:
        # テスト用のゲーム名、URL、質問
        test_game_name = "ゼルダの伝説 ティアーズ オブ ザ キングダム"
        test_url = "https://www.nintendo.co.jp/zelda/totk/guide/" # テスト用URL

        initial_question = "序盤でバッテリーを効率的に増やすにはどうすれば良いですか？"
        
        # 最初のユーザーのターンに、ゲーム名とURL情報を埋め込んだプロンプトを構築
        first_user_prompt = f"""
        あなたはゲーム攻略アシスタントです。ユーザーの質問に対し、提供されたURL（{test_url}）の情報を最優先に参照し、そのURLから回答が得られない場合や、より補足情報が必要な場合のみWeb検索（Grounding機能）を活用して、最も適切で役立つ攻略情報を提供してください。
        回答は日本のゲームプレイヤー向けに、分かりやすく、整理された自然な日本語で提供してください。

        ---
        **ゲーム名:** {test_game_name}
        ---
        ユーザーからの質問: {initial_question}
        """
        
        # 会話履歴の初期化
        conversation_history = [
            {"role": "user", "parts": [first_user_prompt]}
        ]

        print(f"\n--- Gemini AIに問い合わせ中 ---")
        print(f"ゲーム名: {test_game_name}")
        print(f"質問: {initial_question}")
        print(f"参照URL: {test_url}")

        gemini_response = ask_gemini(gemini_model, conversation_history)

        print("\n--- Geminiからの回答 ---")
        if gemini_response:
            print(gemini_response)
            # 2回目の質問の例 (テスト用)
            conversation_history.append({"role": "model", "parts": [gemini_response]})
            next_question = "ウルトラハンドとスクラビルドのコツを教えてください。"
            conversation_history.append({"role": "user", "parts": [next_question]})
            print(f"\n--- 2回目の質問 ---")
            print(f"質問: {next_question}")
            gemini_response_2 = ask_gemini(gemini_model, conversation_history)
            print("\n--- Geminiからの2回目の回答 ---")
            if gemini_response_2:
                print(gemini_response_2)
            else:
                print("2回目の回答取得に失敗しました。")
        else:
            print("Gemini APIからの回答取得に失敗しました。")
    else:
        print("Geminiモデルの初期化に失敗したため、処理を中断します。")
