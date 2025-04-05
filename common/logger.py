#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler
import datetime


class Logger:
    """
    日志记录器类，支持输出到控制台和文件
    使用单例模式确保整个应用中只有一个日志实例
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, log_level=logging.INFO, log_dir=None, log_name=None):
        # 避免重复初始化
        if self._initialized:
            return
            
        self.logger = logging.getLogger('himool_auto_case')
        self.logger.setLevel(log_level)
        self.logger.handlers = []
        
        # 设置日志格式
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器
        if log_dir is None:
            # 获取项目根目录下的logs文件夹
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_dir = os.path.join(project_root, 'logs')
        
        # 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 默认日志文件名
        if log_name is None:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            log_name = f'runtime_{today}.log'
        
        log_file = os.path.join(log_dir, log_name)
        
        # 使用RotatingFileHandler，限制单个日志文件大小
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        self._initialized = True
    
    def get_logger(self):
        """
        获取logger实例
        """
        return self.logger


# 便捷函数，用于获取logger实例
def get_logger(log_level=logging.INFO, log_dir=None, log_name=None):
    """
    获取日志记录器
    :param log_level: 日志级别，默认INFO
    :param log_dir: 日志目录，默认为项目根目录下的logs文件夹
    :param log_name: 日志文件名，默认为runtime_当前日期.log
    :return: logger实例
    """
    logger_instance = Logger(log_level, log_dir, log_name)
    return logger_instance.get_logger()


# 使用示例
if __name__ == '__main__':
    logger = get_logger()
    logger.info('这是一条信息日志')
    logger.warning('这是一条警告日志')
    logger.error('这是一条错误日志')