from handson_celery.config import celery_app
from celery import shared_task
import requests

# 基本的なタスク定義
@celery_app.task
def multiply(x, y):
    """二つの数値を乗算するタスク"""
    return x * y

# レート制限を持つタスク
@celery_app.task(rate_limit='5/m')
def rate_limited_task(value):
    """1分間に最大5回まで実行できるタスク"""
    return f"レート制限付きタスクが {value} を処理しました"

# 結果を無視するタスク
@celery_app.task(ignore_result=True)
def log_task(message):
    """結果を保存しないログ記録タスク"""
    print(f"ログ: {message}")
    # 結果は保存されない

# 自動リトライを持つタスク
@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def fetch_url(url):
    """指定されたURLからデータを取得するタスク（失敗時に自動リトライ）"""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}, status code: {response.status_code}")
    return response.text[:100]  # 最初の100文字だけ返す

# shared_taskデコレータを使用したタスク
@shared_task
def power(x, y):
    """xのy乗を計算するタスク"""
    return x ** y
