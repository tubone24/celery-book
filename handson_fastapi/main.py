from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult

# 新しいパッケージ名でインポート
from handson_celery.config import celery_app
from handson_celery.tasks.task_01.simple_tasks import add

app = FastAPI(title="FastAPI with Celery ハンズオン")

class AdditionRequest(BaseModel):
    x: int
    y: int

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Celery ハンズオン"}

@app.post("/add/")
async def add_numbers(request: AdditionRequest):
    """足し算タスクを実行するエンドポイント"""
    task = add.delay(request.x, request.y)
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    """タスクの結果を取得するエンドポイント"""
    result = AsyncResult(task_id, app=celery_app)
    if result.ready():
        return {"status": result.status, "result": result.get()}
    return {"status": result.status}
