from handson_celery.config import celery_app

@celery_app.task
def add(x, y):
    """2つの数値を足し算するシンプルなタスク"""
    return x + y
