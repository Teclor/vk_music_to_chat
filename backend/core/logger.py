import logging
from logging.handlers import TimedRotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("vk_app")
logger.setLevel(logging.INFO)

if not logger.handlers:
    # Ежедневная ротация логов
    file_handler = TimedRotatingFileHandler(
        filename="logs/app.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.suffix = "%Y-%m-%d"
    
    console_handler = logging.StreamHandler()
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
