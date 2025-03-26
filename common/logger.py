#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler
from config.settings import LOG_DIR, LOG_LEVEL

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

# 日志文件路径
log_file = os.path.join(LOG_DIR, 'test.log')

# 创建日志记录器
logger = logging.getLogger('test_framework')

# 设置日志级别
log_level = getattr(logging, LOG_LEVEL.upper())
logger.setLevel(log_level)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

# 创建文件处理器
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(log_level)

# 创建日志格式器
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 设置处理器格式
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 添加处理器到记录器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 防止日志重复输出
logger.propagate = False