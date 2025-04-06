#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: Pytest 全局 Fixture 配置

import os
import pytest
import configparser
from datetime import datetime
import pytest_html
from playwright.sync_api import sync_playwright

from common.api_client import ApiClient
from common.logger import get_logger

# 配置报告目录
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
HTML_REPORT_DIR = os.path.join(REPORT_DIR, 'html_report')
ALLURE_REPORT_DIR = os.path.join(REPORT_DIR, 'allure_report')

# 确保报告目录存在
def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


ensure_dir_exists(HTML_REPORT_DIR)
ensure_dir_exists(ALLURE_REPORT_DIR)

# 配置HTML报告元数据
def pytest_configure(config):
    # 新版pytest中使用不同的方式设置元数据
    metadata = getattr(config, '_metadata', {})
    metadata['项目名称'] = 'Himool自动化测试'
    metadata['测试环境'] = 'localhost'
    metadata['执行时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 自定义HTML报告样式
def pytest_html_report_title(report):
    report.title = "Himool自动化测试报告"

# 修改HTML报告中的环境信息表格
def pytest_html_results_table_header(cells):
    cells.insert(1, '<th>描述</th>')
    cells.pop()

def pytest_html_results_table_row(report, cells):
    cells.insert(1, f'<td>{report.description}</td>')
    cells.pop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)

# 测试会话结束后的处理
def pytest_sessionfinish(session, exitstatus):
    print(f"\n测试执行完成，退出状态: {exitstatus}")
    print(f"HTML报告路径: {HTML_REPORT_DIR}")
    print(f"Allure报告路径: {ALLURE_REPORT_DIR}")


# 配置文件读取
@pytest.fixture(scope="session")
def config():
    """
    读取配置文件，返回配置对象
    :return: 配置对象
    """
    config_parser = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'config.ini')
    config_parser.read(config_path, encoding='utf-8')
    
    # 默认使用TEST环境配置
    env = os.environ.get('TEST_ENV', 'TEST')
    
    # 合并DEFAULT和指定环境的配置
    merged_config = dict(config_parser['DEFAULT'])
    if env in config_parser:
        merged_config.update(dict(config_parser[env]))
    
    return merged_config


# 日志fixture
@pytest.fixture(scope="session")
def logger():
    """
    获取日志记录器
    :return: logger实例
    """
    return get_logger()


# API客户端fixture
@pytest.fixture(scope="session")
def api(config, logger):
    """
    创建API客户端实例
    :param config: 配置对象
    :param logger: 日志记录器
    :return: ApiClient实例
    """
    # 如果配置中有api_base_url，则使用它替换base_url
    if 'api_base_url' in config:
        api_config = config.copy()
        api_config['base_url'] = config['api_base_url']
    else:
        api_config = config
        
    api_client = ApiClient(api_config, logger)
    yield api_client


# Playwright浏览器和页面fixture
@pytest.fixture(scope="function")
def page(config, logger):
    """
    创建Playwright浏览器和页面实例
    :param config: 配置对象
    :param logger: 日志记录器
    :return: Page实例
    """
    browser_type = config.get('browser_type', 'chromium')
    headless = config.get('headless', 'True').lower() == 'true'
    
    logger.info(f"启动浏览器: {browser_type}, headless: {headless}")
    
    playwright = sync_playwright().start()
    
    # 根据配置选择浏览器类型
    if browser_type.lower() == 'firefox':
        browser = playwright.firefox.launch(headless=headless)
    elif browser_type.lower() == 'webkit':
        browser = playwright.webkit.launch(headless=headless)
    else:  # 默认使用chromium
        browser = playwright.chromium.launch(headless=headless)
    
    # 创建上下文和页面
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent=config.get('user_agent', None)
    )
    
    # 设置超时
    context.set_default_timeout(int(config.get('timeout', 30000)))
    
    page_obj = context.new_page()
    
    # 返回页面对象
    yield page_obj
    
    # 测试结束后关闭浏览器
    logger.info("关闭浏览器")
    context.close()
    browser.close()
    playwright.stop()