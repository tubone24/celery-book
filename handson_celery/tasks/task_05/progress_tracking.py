from handson_celery.config import celery_app
import time
import random

@celery_app.task(bind=True)
def progress_task(self, total_items=100):
    """
    進捗状況を報告するタスク
    
    update_stateメソッドを使用して進捗状況を報告します
    """
    print(f"進捗報告タスクを開始します。合計アイテム数: {total_items}")
    
    # 初期状態を設定
    self.update_state(
        state='PROGRESS',
        meta={
            'current': 0,
            'total': total_items,
            'percent': 0,
            'status': '処理を開始しています...'
        }
    )
    
    # 各アイテムの処理をシミュレート
    for i in range(total_items):
        # 各アイテムの処理時間をランダムに設定（0.05〜0.15秒）
        processing_time = random.uniform(0.05, 0.15)
        time.sleep(processing_time)
        
        # 10アイテムごとに進捗状況を更新
        if (i + 1) % 10 == 0 or i == total_items - 1:
            percent = int(100.0 * (i + 1) / total_items)
            self.update_state(
                state='PROGRESS',
                meta={
                    'current': i + 1,
                    'total': total_items,
                    'percent': percent,
                    'status': f'アイテム {i + 1}/{total_items} を処理中...'
                }
            )
            print(f"進捗状況: {percent}% ({i + 1}/{total_items})")
    
    # 最終結果を返す
    return {
        'current': total_items,
        'total': total_items,
        'percent': 100,
        'status': '処理が完了しました',
        'result': f'合計 {total_items} アイテムの処理が完了しました'
    }

@celery_app.task(bind=True)
def simulation_task(self, task_type):
    """
    異なる種類のタスク処理をシミュレートするタスク
    
    カスタム状態を使用して様々な状態遷移を示します
    """
    states = {
        'data_processing': ['EXTRACTING', 'TRANSFORMING', 'LOADING', 'SUCCESS'],
        'image_analysis': ['PREPROCESSING', 'ANALYZING', 'POSTPROCESSING', 'SUCCESS'],
        'report_generation': ['COLLECTING', 'COMPILING', 'FORMATTING', 'SUCCESS']
    }
    
    if task_type not in states:
        return {'status': 'ERROR', 'message': f'不明なタスクタイプ: {task_type}'}
    
    task_states = states[task_type]
    total_states = len(task_states)
    
    for i, state in enumerate(task_states):
        # 現在の状態を更新
        self.update_state(
            state=state,
            meta={
                'phase': i + 1,
                'total_phases': total_states,
                'description': f'{state} フェーズを実行中...'
            }
        )
        
        print(f"タスク状態: {state} ({i + 1}/{total_states})")
        
        # 各フェーズの処理をシミュレート
        time.sleep(random.uniform(1.0, 3.0))
    
    # 最終結果を返す
    return {
        'status': 'COMPLETED',
        'message': f'{task_type} タスクが正常に完了しました',
        'phases_completed': total_states
    }
