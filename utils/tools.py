from datetime import datetime
import logging
import os


def _get_function_logger(func_name):
    logger = logging.getLogger(func_name)
    logger.setLevel(logging.ERROR)

    # Evita adicionar múltiplos handlers se o logger já estiver configurado
    if not logger.handlers:
        os.makedirs('errors', exist_ok=True)
        handler = logging.FileHandler(f"errors/{func_name}_error_log.txt")
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def log_retry_error(retry_state):
    func_name = retry_state.fn.__name__
    exception = retry_state.outcome.exception()
    logger = _get_function_logger(func_name)
    logger.error("Function: %s - Error: %s", func_name, str(exception))

def save(file_name: str, file_content:str):
    if 'error' in file_name:
        file_content = f'[{datetime.now().strftime('%d/%m/%Y %H:%M')}] {file_content}'
    with open(file_name, 'a', encoding='utf-8') as log_file:
        log_file.write(file_content)

