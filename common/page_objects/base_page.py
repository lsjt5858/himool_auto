#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from playwright.sync_api import Page, expect
from common.logger import logger
from common.allure_report import attach_screenshot
from config.settings import TIMEOUT

class BasePage:
    """页面对象模型基类
    
    所有页面类的基类，提供通用的页面操作方法。
    """
    
    def __init__(self, page: Page):
        """初始化页面对象
        
        Args:
            page: Playwright页面对象
        """
        self.page = page
        self.timeout = TIMEOUT * 1000  # 转换为毫秒
    
    def navigate(self, url):
        """导航到指定URL
        
        Args:
            url: 目标URL
        """
        logger.info(f"导航到 {url}")
        self.page.goto(url)
    
    def wait_for_selector(self, selector, state="visible", timeout=None):
        """等待元素出现
        
        Args:
            selector: 元素选择器
            state: 元素状态，可选值：'attached', 'detached', 'visible', 'hidden'
            timeout: 超时时间（毫秒）
            
        Returns:
            Locator: 元素定位器
        """
        timeout = timeout or self.timeout
        logger.debug(f"等待元素 {selector} {state}")
        return self.page.wait_for_selector(selector, state=state, timeout=timeout)
    
    def wait_for_navigation(self, url=None, wait_until="load", timeout=None):
        """等待页面导航完成
        
        Args:
            url: 预期URL，可以是字符串或正则表达式
            wait_until: 等待条件，可选值：'load', 'domcontentloaded', 'networkidle'
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.debug(f"等待导航完成，条件: {wait_until}")
        if url:
            self.page.wait_for_url(url, wait_until=wait_until, timeout=timeout)
        else:
            self.page.wait_for_load_state(wait_until, timeout=timeout)
    
    def click(self, selector, force=False, timeout=None):
        """点击元素
        
        Args:
            selector: 元素选择器
            force: 是否强制点击
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.debug(f"点击元素 {selector}")
        self.page.click(selector, force=force, timeout=timeout)
    
    def fill(self, selector, value, timeout=None):
        """填充输入框
        
        Args:
            selector: 元素选择器
            value: 输入值
            timeout: 超时时间（毫秒）
        """
        timeout = timeout or self.timeout
        logger.debug(f"填充元素 {selector} 值为 {value}")
        self.page.fill(selector, value, timeout=timeout)
    
    def type(self, selector, text, delay=100, timeout=None):
        """模拟键盘输入
        
        Args:
            selector: 元素选择器
            text: 输入文本
            delay: 输入延迟（毫秒）
            timeout: 超时时间（毫秒）