# ベースイメージの指定
FROM python:3.10-slim

# 作業ディレクトリの作成
WORKDIR /app

# 必要なファイルをコピー
COPY . .

# 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリケーションの実行
CMD ["python", "app.py"]