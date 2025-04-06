#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: Pytest 全局 Fixture 配置

import os
import pytest
from datetime import datetime
import pytest_html
from common.api_client import ApiClient

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

# API客户端session级别fixture
@pytest.fixture(scope="session")
def api_client():
    """
    创建API客户端并登录，整个测试会话共享同一个客户端实例和登录token
    """
    client = ApiClient(base_url="http://localhost:8080")
    # 登录系统获取token
    response = client.login(username="admin", password="Lx123456", number="001")
    assert response.status_code == 200, "登录失败，无法获取token"
    assert client.access_token, "登录成功但未获取到access token"
    
    return client

# 测试会话结束后的处理
def pytest_sessionfinish(session, exitstatus):
    print(f"\n测试执行完成，退出状态: {exitstatus}")
    print(f"HTML报告路径: {HTML_REPORT_DIR}")
    print(f"Allure报告路径: {ALLURE_REPORT_DIR}")