import os
import logging
from logging.handlers import RotatingFileHandler
import sys
import time
from config.settings import LOG_LEVEL, LOG_FORMAT, LOG_FILE_PATH, BASE_DIR

# 确保日志目录存在
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# 创建日志记录器
logger = logging.getLogger('himool_auto_case')
logger.setLevel(getattr(logging, LOG_LEVEL))

# 创建控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, LOG_LEVEL))
console_formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(console_formatter)

# 创建文件处理器
file_handler = RotatingFileHandler(
    LOG_FILE_PATH,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(getattr(logging, LOG_LEVEL))
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)

# 添加处理器到记录器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def get_logger():
    """获取日志记录器"""
    return logger