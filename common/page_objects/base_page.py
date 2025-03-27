from playwright.sync_api import Page, expect
from common.logger import get_logger
from config.settings import UI_URL, UI_TIMEOUT

logger = get_logger()

class BasePage:
    """页面对象基类"""
    
    def __init__(self, page: Page, base_url=None):
        self.page = page
        self.base_url = base_url or UI_URL
        self.timeout = UI_TIMEOUT
    
    def navigate(self, path=""):
        """导航到指定页面"""
        url = f"{self.base_url}{path}"
        logger.info(f"导航到页面: {url}")
        self.page.goto(url, timeout=self.timeout)
        return self
    
    def wait_for_load_state(self, state="networkidle"):
        """等待页面加载状态"""
        logger.info(f"等待页面加载状态: {state}")
        self.page.wait_for_load_state(state)
        return self
    
    def get_element(self, selector, timeout=None):
        """获取元素"""
        timeout = timeout or self.timeout
        logger.info(f"获取元素: {selector}")
        return self.page.locator(selector).first
    
    def click(self, selector, timeout=None, force=False):
        """点击元素"""
        timeout = timeout or self.timeout
        logger.info(f"点击元素: {selector}")
        self.page.locator(selector).first.click(timeout=timeout, force=force)
        return self
    
    def fill(self, selector, value, timeout=None):
        """填充输入框"""
        timeout = timeout or self.timeout
        logger.info(f"填充输入框 {selector}: {value}")
        self.page.locator(selector).first.fill(value, timeout=timeout)
        return self
    
    def select_option(self, selector, value=None, label=None, index=None, timeout=None):
        """选择下拉选项"""
        timeout = timeout or self.timeout
        logger.info(f"选择下拉选项 {selector}: value={value}, label={label}, index={index}")
        
        if value:
            self.page.locator(selector).select_option(value=value, timeout=timeout)
        elif label:
            self.page.locator(selector).select_option(label=label, timeout=timeout)
        elif index is not None:
            self.page.locator(selector).select_option(index=index, timeout=timeout)
        
        return self
    
    def get_text(self, selector, timeout=None):
        """获取元素文本"""
        timeout = timeout or self.timeout
        logger.info(f"获取元素文本: {selector}")
        return self.page.locator(selector).first.text_content(timeout=timeout)
    
    def is_visible(self, selector, timeout=None):
        """判断元素是否可见"""
        timeout = timeout or self.timeout
        logger.info(f"判断元素是否可见: {selector}")
        return self.page.locator(selector).first.is_visible(timeout=timeout)
    
    def wait_for_selector(self, selector, state="visible", timeout=None):
        """等待元素出现"""
        timeout = timeout or self.timeout
        logger.info(f"等待元素 {selector} 状态为 {state}")
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
        return self
    
    def take_screenshot(self, path=None):
        """截图"""
        if not path:
            import time
            path = f"reports/screenshots/screenshot_{int(time.time())}.png"
        
        logger.info(f"截图保存到: {path}")
        self.page.screenshot(path=path)
        return self
    
    def expect_element(self, selector, to_be_visible=True, timeout=None):
        """断言元素可见性"""
        timeout = timeout or self.timeout
        logger.info(f"断言元素 {selector} 可见性为 {to_be_visible}")
        
        if to_be_visible:
            expect(self.page.locator(selector).first).to_be_visible(timeout=timeout)
        else:
            expect(self.page.locator(selector).first).not_to_be_visible(timeout=timeout)
        
        return self
    
    def expect_text(self, selector, text, timeout=None):
        """断言元素文本内容"""
        timeout = timeout or self.timeout
        logger.info(f"断言元素 {selector} 文本为 {text}")
        expect(self.page.locator(selector).first).to_contain_text(text, timeout=timeout)
        return self