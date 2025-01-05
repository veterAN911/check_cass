import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # уровень логирования
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('parser_log.log'),  # файл для записи логов
            logging.StreamHandler()  # вывод в консоль
        ]
    )