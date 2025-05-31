from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from celery.result import AsyncResult

from handson_celery.config import celery_app
from handson_celery.tasks.task_02.task_definitions import multiply, rate_limited_task, fetch_url, power
from handson_celery.tasks.task_02.error_handling import unreliable_task, auto_retry_task, task_with_expected_errors
from handson_celery.tasks.task_04.task_control import scheduled_task, priority_task, time_limited_task
from handson_celery.tasks.task_05.progress_tracking import progress_task, simulation_task
from handson_celery.tasks.task_06.task_workflows import chain_example, group_example, chord_example, complex_workflow_example

router = APIRouter(prefix="/tasks", tags=["tasks"])

# 基本的なリクエストモデル
class MathRequest(BaseModel):
    x: float
    y: float

class ValueRequest(BaseModel):
    value: Any

class UrlRequest(BaseModel):
    url: str

class TaskTypeRequest(BaseModel):
    task_type: str

class ProgressRequest(BaseModel):
    total_items: int = 100

# 基本的なタスク
@router.post("/multiply")
async def multiply_numbers(request: MathRequest):
    """乗算タスクを実行するエンドポイント"""
    task = multiply.delay(request.x, request.y)
    return {"task_id": task.id}

@router.post("/power")
async def calculate_power(request: MathRequest):
    """べき乗タスクを実行するエンドポイント"""
    task = power.delay(request.x, request.y)
    return {"task_id": task.id}

@router.post("/rate-limited")
async def rate_limited(request: ValueRequest):
    """レート制限付きタスクを実行するエンドポイント"""
    task = rate_limited_task.delay(request.value)
    return {"task_id": task.id, "message": "レート制限付きタスクが送信されました（1分間に最大5回）"}

@router.post("/fetch-url")
async def fetch_url_endpoint(request: UrlRequest):
    """URLからデータを取得するタスクを実行するエンドポイント"""
    task = fetch_url.delay(request.url)
    return {"task_id": task.id}

# エラーハンドリング
@router.post("/unreliable")
async def unreliable_endpoint(request: UrlRequest):
    """信頼性の低いタスクを実行するエンドポイント"""
    task = unreliable_task.delay(request.url)
    return {"task_id": task.id, "message": "信頼性の低いタスクが送信されました（80%の確率で失敗します）"}

@router.post("/auto-retry")
async def auto_retry_endpoint(request: MathRequest):
    """自動リトライタスクを実行するエンドポイント"""
    task = auto_retry_task.delay(request.x, request.y)
    return {"task_id": task.id, "message": "自動リトライタスクが送信されました"}

@router.post("/expected-errors")
async def expected_errors_endpoint(request: ValueRequest):
    """想定内エラーを持つタスクを実行するエンドポイント"""
    task = task_with_expected_errors.delay(request.value)
    return {"task_id": task.id}

# タスク制御
@router.post("/scheduled")
async def scheduled_endpoint():
    """スケジュール実行タスクを実行するエンドポイント"""
    countdown_result, eta_result = scheduled_task.apply_async(
        args=["API呼び出し"],
        countdown=10
    ), scheduled_task.apply_async(
        args=["API呼び出し（ETA）"],
        countdown=20
    )
    
    return {
        "countdown_task_id": countdown_result.id,
        "eta_task_id": eta_result.id,
        "message": "2つのスケジュールタスクが送信されました（10秒後と20秒後）"
    }

@router.post("/priority")
async def priority_endpoint():
    """優先度付きタスクを実行するエンドポイント"""
    low_priority, high_priority = priority_task.apply_async(
        args=["低"],
        priority=1
    ), priority_task.apply_async(
        args=["高"],
        priority=9
    )
    
    return {
        "low_priority_task_id": low_priority.id,
        "high_priority_task_id": high_priority.id,
        "message": "優先度の異なる2つのタスクが送信されました"
    }

@router.post("/time-limited")
async def time_limited_endpoint():
    """時間制限付きタスクを実行するエンドポイント"""
    task = time_limited_task.delay()
    return {
        "task_id": task.id,
        "message": "時間制限付きタスクが送信されました（20秒のソフトリミット、30秒のハードリミット）"
    }

# 進捗追跡
@router.post("/progress")
async def progress_endpoint(request: ProgressRequest):
    """進捗報告タスクを実行するエンドポイント"""
    task = progress_task.delay(request.total_items)
    return {
        "task_id": task.id,
        "message": f"進捗報告タスクが開始されました（{request.total_items}アイテム）"
    }

@router.post("/simulation")
async def simulation_endpoint(request: TaskTypeRequest):
    """シミュレーションタスクを実行するエンドポイント"""
    valid_types = ["data_processing", "image_analysis", "report_generation"]
    
    if request.task_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"無効なタスクタイプです。有効なタイプ: {', '.join(valid_types)}")
    
    task = simulation_task.delay(request.task_type)
    return {
        "task_id": task.id,
        "message": f"{request.task_type} シミュレーションタスクが開始されました"
    }

# ワークフロー
@router.post("/chain")
async def chain_endpoint():
    """タスクチェインを実行するエンドポイント"""
    result = chain_example()
    return {
        "task_id": result.id,
        "message": "タスクチェインが開始されました"
    }

@router.post("/group")
async def group_endpoint():
    """タスクグループを実行するエンドポイント"""
    result = group_example()
    return {
        "task_id": result.id,
        "message": "タスクグループが開始されました"
    }

@router.post("/chord")
async def chord_endpoint():
    """タスクコードを実行するエンドポイント"""
    result = chord_example()
    return {
        "task_id": result.id,
        "message": "タスクコードが開始されました"
    }

@router.post("/complex-workflow")
async def complex_workflow_endpoint():
    """複雑なワークフローを実行するエンドポイント"""
    result = complex_workflow_example()
    return {
        "task_id": result.id,
        "message": "複雑なワークフローが開始されました"
    }

# タスク結果取得
@router.get("/result/{task_id}")
async def get_task_result(task_id: str):
    """タスクの結果を取得するエンドポイント"""
    result = AsyncResult(task_id, app=celery_app)
    
    response = {"task_id": task_id, "status": result.status}
    
    if result.ready():
        if result.successful():
            response["result"] = result.get()
        else:
            response["error"] = str(result.result)
            response["traceback"] = result.traceback
    elif result.status == 'PROGRESS':
        response["progress"] = result.info
    
    return response
