# タスクの定義と実行に関するモジュール
from handson_celery.tasks.task_02.task_definitions import multiply, rate_limited_task, log_task, fetch_url, power
from handson_celery.tasks.task_02.execution_modes import process_data, handle_complex_data
from handson_celery.tasks.task_02.error_handling import unreliable_task, auto_retry_task, task_with_expected_errors
