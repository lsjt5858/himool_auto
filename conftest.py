import os
import pytest
import allure
from datetime import datetime
from playwright.sync_api import sync_playwright
from common.logger import get_logger
from common.api_client import APIClient
from common.allure_report import set_allure_environment, attach_screenshot
from config.settings import UI_URL, UI_TIMEOUT

logger = get_logger()

# 设置Allure环境变量
set_allure_environment()

@pytest.fixture(scope="session")
def api_client():
    """API客户端，会话级别"""
    logger.info("创建API客户端")
    client = APIClient()
    yield client
    logger.info("关闭API客户端")

@pytest.fixture(scope="session")
def playwright():
    """Playwright实例，会话级别"""
    logger.info("启动Playwright")
    pw = sync_playwright().start()
    yield pw
    logger.info("关闭Playwright")
    pw.stop()

@pytest.fixture(scope="function")
def browser(playwright):
    """浏览器实例，函数级别"""
    logger.info("创建浏览器实例")
    browser = playwright.chromium.launch(headless=True)
    yield browser
    logger.info("关闭浏览器实例")
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """页面实例，函数级别"""
    logger.info("创建页面实例")
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(UI_TIMEOUT)
    yield page
    logger.info("关闭页面实例")
    page.close()

@pytest.fixture(scope="function")
def logged_in_page(page):
    """已登录的页面实例，函数级别"""
    logger.info("创建已登录的页面实例")
    # 导航到登录页
    page.goto(f"{UI_URL}/login")
    
    # 执行登录
    page.fill("#username", "test_user")
    page.fill("#password", "password123")
    page.click("#login-button")
    
    # 等待登录成功
    page.wait_for_url(f"{UI_URL}/home")
    
    yield page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试结果钩子，用于失败截图"""
    outcome = yield
    report = outcome.get_result()
    
    # 如果是UI测试且测试失败，进行截图
    if "page" in item.funcargs and report.when == "call" and report.failed:
        page = item.funcargs["page"]
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        screenshot_path = f"{screenshot_dir}/failure_{item.name}_{timestamp}.png"
        
        # 截图并添加到Allure报告
        try:
            page.screenshot(path=screenshot_path)
            allure.attach.file(
                screenshot_path,
                name=f"Failure Screenshot: {item.name}",
                attachment_type=allure.attachment_type.PNG
            )
            logger.info(f"测试失败截图保存到: {screenshot_path}")
        except Exception as e:
            logger.error(f"截图失败: {e}")