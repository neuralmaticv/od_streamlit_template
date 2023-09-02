import os
import logging
from logging.handlers import TimedRotatingFileHandler
from config.config import TEMP_LOG_OUT

def setup_logging(log_dir):
    path = os.path.join(TEMP_LOG_OUT, log_dir)
    os.makedirs(path, exist_ok=True)

    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')

    log_handler = TimedRotatingFileHandler(
        filename=os.path.join(path, 'app.log'),
        when='midnight', interval=1, backupCount=7
    )
    log_handler.setFormatter(log_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    return logger
