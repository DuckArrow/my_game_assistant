# Python 3.12 のスリム版イメージをベースとして使用
FROM python:3.12-slim-buster

# Git とその他のビルドに必要なツールをインストール
# apt-get update でパッケージリストを更新し、git をインストールします。
# rm -rf /var/lib/apt/lists/* は、キャッシュを削除してイメージサイズを削減します。
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# リポジトリをクローンするための一時的な作業ディレクトリを設定
# このディレクトリはイメージに含まれますが、必要な作業後に最終的なWORKDIRに移動します。
WORKDIR /tmp

# GitHubリポジトリをクローン
# あなたのリポジトリURLをここに指定してください。
# RUN git clone https://github.com/DuckArrow/my_game_assistant.git
# 上記はあなたのリポジトリURLなので、そのまま使えます。
RUN git clone https://github.com/DuckArrow/my_game_assistant.git

# クローンしたリポジトリのディレクトリを最終的な作業ディレクトリに設定
# これにより、以降のコマンドはこのディレクトリ内で実行されます。
WORKDIR /tmp/my_game_assistant

# requirements.txt から必要なPythonライブラリをインストール
# --no-cache-dir は、キャッシュを保存しないことでイメージサイズを削減します。
RUN pip install --no-cache-dir -r requirements.txt

# Streamlitアプリがリッスンするポート (デフォルトは8501) を公開
EXPOSE 8501

# コンテナ起動時に実行されるコマンド
# Streamlitアプリケーションを起動します。
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# --server.address=0.0.0.0 は、コンテナ外からのアクセスを許可するために重要です。
