# **🎮 ゲーム攻略アシスタント (Gemini AI & Streamlit)**

このプロジェクトは、GoogleのGemini AIとStreamlitを使用して構築された、インタラクティブなゲーム攻略アシスタントです。ユーザーが攻略したいゲーム名と、参考にしたい攻略サイトのURL（任意）を入力すると、Gemini AIがその情報を基に、またはWeb検索（Grounding機能）を活用して質問に答えます。

Webスクレイピングの代わりに、Gemini AIのWeb検索（Grounding）機能に直接URLをヒントとして与えるアプローチを採用しています。

## **✨ 機能**

* **ゲーム攻略の質問応答:** 特定のゲームに関する質問にGemini AIが回答します。  
* **URL参照:** 指定された攻略サイトのURLの情報をGemini AIが優先的に参照し、回答を生成します。  
* **Web検索（Grounding）:** URL情報で不足する場合やURLが入力されていない場合に、Gemini AIが自動的にWeb検索を行い情報を補完します。  
* **チャット形式のUI:** Streamlitによる直感的なWebインターフェースで、継続的な会話が可能です。  
* **セッションリセット:** 会話履歴とゲーム情報をリセットし、新しいゲームの攻略を開始できます。

## **🚀 セットアップと実行方法**

### **1\. リポジトリのクローン**

まず、このGitHubリポジトリをローカルにクローンします。

git clone \[https://github.com/YourUsername/my\_game\_assistant.git\](https://github.com/YourUsername/my\_game\_assistant.git) \# 'YourUsername'をあなたのGitHubユーザー名に変更してください  
cd my\_game\_assistant

### **2\. Python仮想環境のセットアップ**

プロジェクトの依存関係を管理するために、Pythonの仮想環境（venv）を作成してアクティベートすることを強く推奨します。

python3 \-m venv venv  
source venv/bin/activate \# macOS/Linux  
\# .\\venv\\Scripts\\activate \# Windows (PowerShell)

### **3\. 必要なライブラリのインストール**

仮想環境をアクティベートしたら、requirements.txt を使用して必要なPythonライブラリをインストールします。

pip install \-r requirements.txt

### **4\. Gemini APIキーの設定**

Google Gemini APIを利用するには、APIキーが必要です。  
Google AI Studio でAPIキーを取得してください。  
取得したAPIキーは、環境変数として設定することを推奨します。GEMINI\_API\_KEYという名前で設定します。

プロジェクトのルートディレクトリに .env ファイルを作成し、以下の内容を記述してください。

GEMINI\_API\_KEY="ここにあなたのGemini APIキーを貼り付けます"

**重要:** .env ファイルは機密情報を含むため、GitHubにアップロードしないでください。.gitignore に追加しておくのが一般的です。

### **5\. Geminiモデルの選択**

gemini\_assistant.py ファイルを開き、initialize\_gemini\_model 関数内の model\_name を、使用したいGeminiモデル名に変更してください。

例：

* 'gemini-1.5-flash' (高速で費用対効果が高い)  
* 'gemini-1.5-pro' (より高性能)  
* 'gemini-2.5-flash-preview-05-20' (最新のFlashプレビュー版)  
* 'gemini-2.5-pro-preview-05-06' (最新のProプレビュー版、高機能)

\# gemini\_assistant.py 内の initialize\_gemini\_model 関数  
model \= genai.GenerativeModel(model\_name='gemini-2.5-pro-preview-05-06') \# 例

**注意:** プレビュー版モデルは名前が更新されたり、予告なく利用できなくなったりする可能性があります。最新の利用可能なモデル名は、[Google AI Developersの公式ドキュメント](https://ai.google.dev/gemini-api/docs/models) や [リリースノート](https://ai.google.dev/gemini-api/docs/changelog) でご確認ください。また、高性能モデルは費用が高くなる可能性があります。

### **6\. アプリケーションの実行**

すべての設定が完了したら、Streamlitアプリケーションを実行します。

streamlit run streamlit\_app.py

コマンドを実行すると、ターミナルにローカルURLが表示されます (http://localhost:8501 など)。このURLをWebブラウザで開くと、ゲーム攻略アシスタントのUIが表示されます。

## **💡 使用方法**

1. Webブラウザで開かれたアプリの最初の画面で、**攻略したいゲーム名**を入力します。  
2. **参考にしたい攻略サイトや情報のURL**を任意で入力します。（例: https://www.nintendo.co.jp/zelda/totk/guide/）  
   * このURLはアプリ側でスクレイピングされず、Gemini AIに直接参照元として渡されます。  
3. 「アシスタントとのセッションを開始する」ボタンをクリックします。  
4. チャット入力欄が表示されるので、ゲームに関する質問を入力してください。

## **🗑️ web\_scraper.py ファイルについて**

このリポジトリには web\_scraper.py ファイルが含まれていますが、現在の streamlit\_app.py では**このファイルは使用されていません。** 以前のバージョンではWebスクレイピング機能が実装されていましたが、Gemini AIのWeb検索（Grounding）機能をより直接的に活用するアプローチに変更されたため、現在では利用していません。

## **📄 ライセンス**

このプロジェクトはMITライセンスの下で公開されています。
