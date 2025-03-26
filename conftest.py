#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright
from common.api_client import APIClient
from common.logger import logger
from config.settings import DATA_DIR, HTML_REPORT_DIR, USERNAME, PASSWORD, USER_NUMBER

# 确保报告目录存在
os.makedirs(HTML_REPORT_DIR, exist_ok=True)

# 加载测试数据
test_data_path = os.path.join(DATA_DIR, 'test_data.json')
if os.path.exists(test_data_path):
    with open(test_data_path, 'r', encoding='utf-8') as f:
        TEST_DATA = json.load(f)
else:
    TEST_DATA = {}

@pytest.fixture(scope="session")
def api_client():
    """API客户端实例
    
    Returns:
        APIClient: API客户端实例
    """
    client = APIClient()
    logger.info("创建API客户端实例")
    yield client

@pytest.fixture(scope="function")
def logged_in_api_client(api_client):
    """已登录的API客户端实例
    
    Args:
        api_client: API客户端实例
        
    Returns:
        APIClient: 已登录的API客户端实例
    """
    logger.info("使用默认用户登录")
    api_client.login(USER_NUMBER, USERNAME, PASSWORD)
    yield api_client

@pytest.fixture(scope="session")
def browser():
    """Playwright浏览器实例
    
    Returns:
        Browser: 浏览器实例
    """
    logger.info("启动浏览器")
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()
    playwright.stop()
    logger.info("关闭浏览器")

@pytest.fixture(scope="function")
def page(browser):
    """Playwright页面实例
    
    Args:
        browser: 浏览器实例
        
    Returns:
        Page: 页面实例
    """
    logger.info("创建新页面")
    page = browser.new_page()
    yield page
    page.close()
    logger.info("关闭页面")

@pytest.fixture(scope="function")
def test_data():
    """测试数据
    
    Returns:
        dict: 测试数据
    """
    return TEST_DATA

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试结果钩子，用于在测试失败时截图
    
    Args:
        item: 测试项
        call: 调用信息
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # 如果测试失败且fixture中有page对象，则截图
        for name, value in item._fixtureinfo.name2fixturedefs.items():
            if name == "page" and hasattr(item, "funcargs") and "page" in item.funcargs:
                page = item.funcargs["page"]
                screenshot_dir = os.path.join(HTML_REPORT_DIR, "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                
                # 生成截图文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.nodeid.replace("/", "_").replace("::", "_")
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
                
                # 截图
                try:
                    page.screenshot(path=screenshot_path)
                    logger.info(f"测试失败截图已保存: {screenshot_path}")
                    
                    # 附加到Allure报告
                    from common.allure_report import attach_screenshot
                    attach_screenshot(page, f"失败截图_{test_name}")
                except Exception as e:
                    logger.error(f"截图失败: {str(e)}")
                    
                # 附加页面HTML到报告
                try:
                    from common.allure_report import attach_html
                    html_content = page.content()
                    attach_html(html_content, f"页面HTML_{test_name}")
                except Exception as e:
                    logger.error(f"附加HTML失败: {str(e)}")