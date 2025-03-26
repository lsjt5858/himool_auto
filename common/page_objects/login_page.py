#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from playwright.sync_api import expect
from common.page_objects.base_page import BasePage
from common.logger import logger
from common.allure_report import attach_screenshot
from config.settings import BASE_URL

class LoginPage(BasePage):
    """登录页面对象
    
    封装登录页面的元素和操作。
    """
    
    # 页面URL
    URL = f"{BASE_URL}/login"
    
    # 页面元素选择器
    NUMBER_INPUT = "#number"
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    LOGIN_FORM = "form.login-form"
    SUCCESS_MESSAGE = ".success-message"
    
    def navigate(self, url=None):
        """导航到登录页面
        
        Args:
            url: 页面URL，默认为登录页面URL
        """
        url = url or self.URL
        super().navigate(url)
        logger.info(f"导航到登录页面: {url}")
    
    def get_title(self):
        """获取页面标题