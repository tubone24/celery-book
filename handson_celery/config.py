from celery import Celery

# Celeryアプリケーションの設定
celery_app = Celery(
    "handson_tasks",
    broker="pyamqp://guest:guest@rabbitmq:5672//",
    backend="redis://redis:6379/0",
)

# タスク設定
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],˚
    result_serializer="json",
    timezone="Asia/Tokyo",
    enable_utc=True,
)

# タスク自動検出設定
celery_app.autodiscover_tasks([
    "handson_celery.tasks.task_01", 
    "handson_celery.tasks.task_02", 
    "handson_celery.tasks.task_03",
    "handson_celery.tasks.task_04",
    "handson_celery.tasks.task_05",
    "handson_celery.tasks.task_06"
])
