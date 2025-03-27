import os
import configparser
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 读取配置文件
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config', 'config.ini'), encoding='utf-8')

# 当前环境
CURRENT_ENV = config.get('env', 'current')

# 环境配置
BASE_URL = config.get(CURRENT_ENV, 'base_url')
UI_URL = config.get(CURRENT_ENV, 'ui_url')
USERNAME = config.get(CURRENT_ENV, 'username')
PASSWORD = config.get(CURRENT_ENV, 'password')
NUMBER = config.get(CURRENT_ENV, 'number')

# 日志配置
LOG_LEVEL = config.get('log', 'level')
LOG_FORMAT = config.get('log', 'format')
LOG_FILE_PATH = os.path.join(BASE_DIR, config.get('log', 'file_path'))

# 报告配置
ALLURE_RESULT_PATH = os.path.join(BASE_DIR, config.get('report', 'allure_result_path'))
HTML_REPORT_PATH = os.path.join(BASE_DIR, config.get('report', 'html_report_path'))

# 超时配置
REQUEST_TIMEOUT = 30
UI_TIMEOUT = 30000  # 毫秒

# 重试配置
MAX_RETRIES = 3