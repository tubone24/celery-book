from handson_celery.config import celery_app

@celery_app.task
def process_data(data):
    """データを処理するタスク"""
    processed = {k: v * 2 for k, v in data.items()}
    return processed

def demonstrate_async_execution():
    """非同期実行のデモンストレーション"""
    # delay()メソッドを使った非同期実行
    data = {"a": 1, "b": 2, "c": 3}
    result = process_data.delay(data)
    
    print("タスク送信完了。結果を待たずに他の処理を継続できます。")
    print(f"タスクID: {result.id}")
    print(f"タスク状態: {result.status}")
    
    # 結果を取得する場合（ブロッキング）
    try:
        value = result.get(timeout=10)  # 最大10秒待つ
        print(f"タスク結果: {value}")
    except celery_app.TimeoutError:
        print("タスクがタイムアウトしました")
    
    return result

def demonstrate_sync_execution():
    """同期実行のデモンストレーション"""
    # apply()メソッドを使った同期実行
    data = {"a": 1, "b": 2, "c": 3}
    result = process_data.apply(args=[data])
    
    print("同期実行が完了しました。")
    print(f"タスク状態: {result.status}")
    print(f"タスク結果: {result.get()}")
    
    return result

@celery_app.task(serializer='json')
def handle_complex_data(data):
    """複雑なデータを処理するタスク"""
    # データはJSONシリアライズ可能である必要がある
    # 例: 整数、浮動小数点数、文字列、リスト、辞書など
    result = {
        "processed": True,
        "input_keys": list(data.keys()),
        "input_values": list(data.values()),
        "input_length": len(data)
    }
    return result
