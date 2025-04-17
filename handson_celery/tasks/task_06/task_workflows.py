from handson_celery.config import celery_app
from celery import chain, group, chord, signature
import time
import random

# 基本的なタスク
@celery_app.task
def add(x, y):
    """2つの数値を足し算するタスク"""
    return x + y

@celery_app.task
def multiply(x, y):
    """2つの数値を掛け算するタスク"""
    return x * y

@celery_app.task
def power(x, y):
    """xのy乗を計算するタスク"""
    return x ** y

@celery_app.task
def process_number(number):
    """数値を処理するタスク"""
    time.sleep(random.uniform(0.1, 0.5))  # 処理時間をシミュレート
    return number * 2

@celery_app.task
def sum_numbers(numbers):
    """数値のリストを合計するタスク"""
    return sum(numbers)

@celery_app.task
def format_result(result):
    """結果を整形するタスク"""
    return f"計算結果: {result}"

# チェイン（chain）の例
def chain_example():
    """
    タスクチェインのデモ
    
    add(2, 2) -> multiply(結果, 3) -> power(結果, 2) -> format_result(結果)
    """
    # チェインの作成方法1: |（パイプ）演算子を使用
    workflow = add.s(2, 2) | multiply.s(3) | power.s(2) | format_result.s()
    
    # チェインの作成方法2: chain関数を使用
    # workflow = chain(add.s(2, 2), multiply.s(3), power.s(2), format_result.s())
    
    print("チェインワークフローを開始します...")
    result = workflow()
    
    return result

# グループ（group）の例
def group_example():
    """
    タスクグループのデモ
    
    複数のprocess_numberタスクを並列実行
    """
    numbers = [1, 2, 3, 4, 5]
    
    # グループの作成
    tasks_group = group(process_number.s(num) for num in numbers)
    
    print("グループワークフローを開始します...")
    result = tasks_group()
    
    return result

# コード（chord）の例
def chord_example():
    """
    タスクコードのデモ
    
    複数のprocess_numberタスクを並列実行し、
    すべて完了したらsum_numbersタスクで結果を集約
    """
    numbers = [1, 2, 3, 4, 5]
    
    # コードの作成: ヘッダー（グループ）とコールバックを指定
    header = group(process_number.s(num) for num in numbers)
    callback = sum_numbers.s()
    
    workflow = chord(header)(callback)
    
    print("コードワークフローを開始します...")
    result = workflow
    
    return result

# チャンク（chunks）の例
def chunks_example():
    """
    タスクチャンクのデモ
    
    大量のタスクをチャンク（塊）に分けて実行
    """
    numbers = list(range(1, 101))  # 1から100までの数値
    
    # チャンクの作成: 10個ずつのタスクに分割
    chunks_workflow = process_number.chunks(zip(numbers), 10)
    
    print("チャンクワークフローを開始します...")
    result = chunks_workflow()
    
    return result

# 複雑なワークフローの例
def complex_workflow_example():
    """
    複雑なワークフローのデモ
    
    チェイン、グループ、コードを組み合わせた複雑なワークフロー
    """
    # 複数の計算を並列実行
    calculations = group(
        add.s(10, 20),
        multiply.s(5, 6),
        power.s(2, 8)
    )
    
    # 結果を合計し、整形する
    workflow = chord(calculations)(
        chain(
            sum_numbers.s(),
            format_result.s()
        )
    )
    
    print("複雑なワークフローを開始します...")
    result = workflow
    
    return result
