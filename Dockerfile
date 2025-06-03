# Python 3.12 のスリム版 Debian Bookworm (Debian 12) イメージをベースとして使用
FROM python:3.12-slim-bookworm

# Git とその他のビルドに必要なツールをインストール
# apt-get update の前に apt-get clean と /var/lib/apt/lists/* を削除
RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

# リポジトリをクローンするための一時的な作業ディレクトリを設定
WORKDIR /tmp

# GitHubリポジトリをクローン
# (DockerfileがGitリポジトリのルートにある場合、通常は不要ですが、
#  アプリコードがGitHubからクローンされる想定で維持しています)
RUN git clone https://github.com/DuckArrow/my_game_assistant.git

# クローンしたリポジトリのディレクトリを最終的な作業ディレクトリに設定
WORKDIR /tmp/my_game_assistant

# requirements.txt から必要なPythonライブラリをインストール
# python-dotenv もここでインストールされます
RUN pip install --no-cache-dir -r requirements.txt

# Streamlitアプリがリッスンするポート (デフォルトは8501) を公開
EXPOSE 8501

# コンテナ起動時に実行されるコマンド
# Streamlitアプリケーションを起動します。
# --server.address=0.0.0.0 は、コンテナ外からのアクセスを許可するために重要です。
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
