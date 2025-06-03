# **🎮 AIゲーム攻略アシスタント**

このプロジェクトは、GoogleのGemini AIを活用したゲーム攻略アシスタントです。ユーザーの質問に対し、指定されたURLの情報を最優先で参照し、必要に応じてWeb検索（Grounding機能）も利用して、役立つ攻略情報を提供します。

## **🚀 プロジェクトのセットアップと実行**

### **1\. 必要要件**

* **Git**: ソースコードのクローン用。  
* **Docker** と **Docker Compose**: アプリケーションの実行環境用。  
* **Google** AI Studio API **キー**: Gemini APIへのアクセスに必要です。  
  * [Google AI Studio](https://aistudio.google.com/) で無料で取得できます。  
  * gemini-1.5-flash モデルには無料枠があります。

### **2\. プロジェクトのクローン**

まず、このGitHubリポジトリをローカルマシンにクローンします。

git clone \[https://github.com/DuckArrow/my\_game\_assistant.git\](https://github.com/DuckArrow/my\_game\_assistant.git)  
cd my\_game\_assistant

### **3\. 環境変数の設定**

Gemini API キーと使用するモデル名を環境変数で設定します。セキュリティのため、.env ファイルを使用し、Gitにはコミットしません。

1. .env.example ファイルを参考に、プロジェクトのルートディレクトリに \*\*.env\*\* という名前でファイルを作成します。  
2. \*\*.env\*\* ファイルに、取得したGemini APIキーとモデル名を以下の形式で記述します。  
   値はダブルクォーテーションで囲まないでください。  
   GEMINI\_API\_KEY=YOUR\_ACTUAL\_GEMINI\_API\_KEY\_HERE  
   GEMINI\_MODEL\_NAME=gemini-1.5-flash

   * YOUR\_ACTUAL\_GEMINI\_API\_KEY\_HERE の部分を、あなたのGoogle AI Studioで生成したAPIキーに置き換えてください。  
   * GEMINI\_MODEL\_NAME は、gemini-1.5-flash（無料枠対応）を推奨しますが、課金設定が有効な場合は他のモデル（例: gemini-1.5-pro、gemini-2.5-flash-preview-05-20 など）も指定可能です。  
3. .gitignore ファイルにはすでに .env が含まれているため、このファイルがGitに誤ってコミットされることはありません。

### **4\. Dockerコンテナのビルドと実行**

プロジェクトをDockerコンテナとしてビルドし、実行します。

1. Dockerイメージのビルド:  
   プロジェクトのルートディレクトリ (my\_game\_assistant ディレクトリ) で、以下のコマンドを実行します。  
   docker build \-t your\_dockerhub\_username/my-game-assistant:latest .

   * your\_dockerhub\_username の部分を、あなたのDocker Hubユーザー名（または任意のタグ名）に置き換えてください。  
2. Dockerコンテナの実行:  
   ビルドしたイメージを使って、.env ファイルから環境変数を読み込み、コンテナを実行します。  
   docker run \-d \-p 8501:8501 \\  
     \--name my-game-assistant \\  
     \--env-file ./.env \\  
     your\_dockerhub\_username/my-game-assistant:latest

   * \--env-file ./.env オプションが、手順3で作成した .env ファイルから環境変数を読み込みます。  
3. アクセス:  
   コンテナが起動したら、Webブラウザで http://localhost:8501 にアクセスしてください。  
   もしリモートサーバーやVM上で実行している場合は、http://\[VMのIPアドレス\]:8501 にアクセスしてください。

### **5\. ホストOSでの直接実行 (開発・デバッグ向け)**

Dockerコンテナを使わずに、直接ホストOSで実行することも可能です。

1. Python環境のセットアップ:  
   Python 3.9以上がインストールされていることを確認してください。  
2. 依存関係のインストール:  
   プロジェクトのルートディレクトリで、requirements.txt に記載されているライブラリをインストールします。  
   pip install \-r requirements.txt

3. 環境変数の設定:  
   手順3で作成した .env ファイルが同じディレクトリにあることを確認してください。gemini\_assistant.py は自動的にこのファイルを読み込みます。  
   または、シェルで直接環境変数を設定することも可能です。  
   export GEMINI\_API\_KEY="YOUR\_ACTUAL\_GEMINI\_API\_KEY\_HERE"  
   export GEMINI\_MODEL\_NAME="gemini-1.5-flash"

4. アプリケーションの実行:  
   以下のコマンドでStreamlitアプリケーションを起動します。  
   streamlit run streamlit\_app.py

## **🛠️ プロジェクト構造**

* Dockerfile: Dockerイメージをビルドするための設定ファイル。  
* requirements.txt: Pythonの依存関係リスト。  
* gemini\_assistant.py: Gemini APIとの主要なインタラクション（モデルの初期化、AIへの問い合わせなど）を処理するスクリプト。  
* streamlit\_app.py: Streamlitフレームワークを使用してWebインターフェースを構築するメインアプリケーションファイル。  
* .env.example: .env ファイル作成のためのテンプレート。  
* .gitignore: Gitのバージョン管理から除外するファイル（.env など）。
