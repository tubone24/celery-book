FROM python:3.11

WORKDIR /app

# uvをインストール
RUN pip install uv

# プロジェクトをコピー
COPY . /app

# uvを使用してプロジェクトをパッケージとしてインストール
RUN uv pip install --system -e .

CMD ["uvicorn", "handson_fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
