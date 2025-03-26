#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import configparser
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 配置文件路径
CONFIG_FILE = os.path.join(ROOT_DIR, 'config', 'config.ini')

# 读取配置文件
config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding='utf-8')

# 获取当前环境
ENV = config['ENV']['env']

# 根据环境获取对应配置
BASE_URL = config[ENV.upper()]['base_url']
USERNAME = config[ENV.upper()]['username']
PASSWORD = config[ENV.upper()]['password']
USER_NUMBER = config[ENV.upper()]['user_number']

# 全局超时设置
TIMEOUT = int(config['DEFAULT']['timeout'])

# 日志级别
LOG_LEVEL = config['DEFAULT']['log_level']

# 日志目录
LOG_DIR = os.path.join(ROOT_DIR, 'logs')

# 报告目录
REPORT_DIR = os.path.join(ROOT_DIR, 'reports')
HTML_REPORT_DIR = os.path.join(REPORT_DIR, 'html_report')
PRESSURE_REPORT_DIR = os.path.join(REPORT_DIR, 'pressure_report')

# 测试数据目录
DATA_DIR = os.path.join(ROOT_DIR, 'data')