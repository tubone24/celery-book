# Celery FastAPI ハンズオン

FastAPIとCeleryを使用した非同期タスク処理のハンズオンプロジェクトです。

## プロジェクト構成

```
celery-fastapi-handson/
├── docker-compose.yml
├── requirements.txt
├── Dockerfile
├── pyproject.toml
├── handson_fastapi/
│   ├── __init__.py
│   └── main.py
└── handson_celery/
    ├── __init__.py
    ├── config.py
    ├── worker.py
    └── tasks/
        ├── __init__.py
        └── task_01/
            ├── __init__.py
            └── simple_tasks.py
```

## uvを使用したインストール方法

このプロジェクトは、uvを使用して開発モードでインストールすることができます。これにより、`handson_celery.`や`handson_fastapi.`などのインポートが正しく動作するようになります。

```bash
# uvのインストール（まだインストールしていない場合）
pip install uv

# 開発モードでプロジェクトをインストール
uv pip install -e .
```

## Docker Composeでの起動方法

```bash
docker-compose up --build
```

## ローカル環境での起動方法

### RabbitMQとRedisの起動

```bash
docker-compose up -d rabbitmq redis
```

### FastAPIアプリケーションの起動

```bash
uvicorn handson_fastapi.main:app --host 0.0.0.0 --port 8000 --reload
```

### Celeryワーカーの起動

```bash
celery -A handson_celery.worker worker --loglevel=info
```

### Flowerの起動（オプション）

```bash
celery -A handson_celery.worker flower --port=5555
```

## 環境変数の設定

ローカル環境では、以下の環境変数を設定する必要があります：

```bash
# macOS/Linux
export CELERY_BROKER_URL=pyamqp://guest:guest@localhost:5672//
export CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Windows (PowerShell)
$env:CELERY_BROKER_URL = "pyamqp://guest:guest@localhost:5672//"
$env:CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
```

## APIエンドポイント

- トップページ: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs
- 足し算タスク: POST http://localhost:8000/add/
- タスク結果確認: GET http://localhost:8000/result/{task_id}

## モニタリング

- Flower: http://localhost:5555
- RabbitMQ管理画面: http://localhost:15672 (ユーザー名: guest, パスワード: guest)
