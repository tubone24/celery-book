from handson_celery.config import celery_app
from datetime import datetime, timedelta
import time

# スケジュール実行（ETA・カウントダウン）のデモ
@celery_app.task
def scheduled_task(arg):
    """スケジュール実行されるタスク"""
    now = datetime.now()
    return f"スケジュールされたタスクが {now.strftime('%Y-%m-%d %H:%M:%S')} に実行されました。引数: {arg}"

def schedule_task_demo():
    """タスクのスケジュール実行をデモンストレーションする関数"""
    # 10秒後に実行（カウントダウン）
    countdown_result = scheduled_task.apply_async(
        args=["カウントダウン"],
        countdown=10
    )
    print(f"タスクがスケジュールされました（10秒後）。タスクID: {countdown_result.id}")
    
    # 特定の時刻に実行（ETA）
    eta_time = datetime.now() + timedelta(seconds=20)
    eta_result = scheduled_task.apply_async(
        args=["ETA"],
        eta=eta_time
    )
    print(f"タスクがスケジュールされました（{eta_time}）。タスクID: {eta_result.id}")
    
    return countdown_result, eta_result

# 優先度付きタスク
@celery_app.task
def priority_task(priority_level):
    """優先度付きで実行されるタスク"""
    return f"優先度 {priority_level} のタスクが実行されました"

def priority_task_demo():
    """タスクの優先度をデモンストレーションする関数"""
    # 優先度の低いタスク（RabbitMQでは0が最低、9が最高）
    low_priority = priority_task.apply_async(
        args=["低"],
        priority=1
    )
    
    # 優先度の高いタスク
    high_priority = priority_task.apply_async(
        args=["高"],
        priority=9
    )
    
    print("優先度の異なる2つのタスクが送信されました")
    print(f"低優先度タスクID: {low_priority.id}")
    print(f"高優先度タスクID: {high_priority.id}")
    
    return low_priority, high_priority

# 時間制限付きタスク
@celery_app.task(time_limit=30, soft_time_limit=20)
def time_limited_task():
    """時間制限付きタスク"""
    try:
        print("時間制限付きタスクを開始します...")
        for i in range(25):
            print(f"処理中... {i}/25")
            time.sleep(1)  # 1秒間スリープ
    except celery_app.exceptions.SoftTimeLimitExceeded:
        print("ソフトタイムリミットを超過しました。クリーンアップを実行します。")
        return "ソフトタイムリミットで中断されました"
    
    return "タスクが正常に完了しました"

# タスクのルーティング
@celery_app.task(queue='image_processing')
def process_image(image_data):
    """画像処理タスク（特定のキューに送信される）"""
    print(f"画像処理を開始します: サイズ {len(image_data)} バイト")
    # 画像処理のシミュレーション
    time.sleep(2)
    return f"画像処理が完了しました: サイズ {len(image_data)} バイト"

@celery_app.task(queue='mail_queue')
def send_email(to, subject, body):
    """メール送信タスク（特定のキューに送信される）"""
    print(f"メール送信: 宛先={to}, 件名={subject}")
    # メール送信のシミュレーション
    time.sleep(1)
    return f"メールが {to} に送信されました"
