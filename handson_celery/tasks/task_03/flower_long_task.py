from handson_celery.config import celery_app
import time
import random

@celery_app.task
def longlong_task():
    """
    長時間実行されるタスクのシミュレーション
    """
    print("長時間タスクを開始します...")

    # タスクの合計実行時間（秒）
    total_duration = 60

    # 進捗報告の間隔（秒）
    report_interval = 5

    start_time = time.time()
    end_time = start_time + total_duration

    # 現在の進捗率
    progress = 0

    while time.time() < end_time:
        # ランダムな計算処理を行う（CPUに負荷をかける）
        for _ in range(1000000):
            _ = random.random() ** 2

        # 経過時間から進捗率を計算
        elapsed = time.time() - start_time
        progress = min(100, int((elapsed / total_duration) * 100))

        # 定期的に進捗を報告
        print(f"タスク進捗: {progress}%")

        # 次の報告まで待機
        time.sleep(report_interval)

    print("長時間タスクが完了しました！")
    return {"status": "completed", "message": "長時間タスクが正常に完了しました"}