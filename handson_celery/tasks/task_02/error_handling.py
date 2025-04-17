from handson_celery.config import celery_app
import random

@celery_app.task(bind=True, max_retries=5, default_retry_delay=60)
def unreliable_task(self, url):
    """
    信頼性の低いタスク - 明示的なリトライ機能を示す
    
    bind=True: タスク関数の第1引数としてタスクインスタンス(self)を受け取る
    max_retries: 最大リトライ回数
    default_retry_delay: リトライ間のデフォルト待機時間（秒）
    """
    try:
        # 80%の確率で失敗するシミュレーション
        if random.random() < 0.8:
            raise Exception("ランダムなエラーが発生しました")
        
        # 成功した場合
        return f"{url} の処理に成功しました"
    
    except Exception as exc:
        # 現在のリトライ回数を取得
        retries = self.request.retries
        
        print(f"エラーが発生しました。リトライ回数: {retries}/{self.max_retries}")
        
        # リトライ上限に達していない場合は再試行
        if retries < self.max_retries:
            # 30秒後に再試行（countdown引数でデフォルト値を上書き）
            raise self.retry(exc=exc, countdown=30)
        
        # リトライ上限に達した場合は例外を再送出
        raise

@celery_app.task(autoretry_for=(ZeroDivisionError,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def auto_retry_task(x, y):
    """
    自動リトライ機能を持つタスク
    
    autoretry_for: 指定した例外が発生した場合に自動的にリトライする
    retry_kwargs: リトライのパラメータを指定
    """
    print(f"{x} / {y} を計算します")
    return x / y  # yが0の場合、ZeroDivisionErrorが発生し自動リトライされる

@celery_app.task(throws=(ValueError, TypeError))
def task_with_expected_errors(value):
    """
    想定内のエラーを指定したタスク
    
    throws: これらの例外はエラーとしてマークされるが、予期されたものとして扱われる
    """
    if not isinstance(value, int):
        raise TypeError("整数を入力してください")
    
    if value < 0:
        raise ValueError("正の整数を入力してください")
    
    return value * 2
