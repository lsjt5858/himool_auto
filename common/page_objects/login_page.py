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
        
        Returns:
            str: 页面标题
        """
        return self.page.title()
    
    def login(self, number, username, password):
        """执行登录操作
        
        Args:
            number: 用户编号
            username: 用户名
            password: 密码
            
        Returns:
            bool: 登录是否成功
        """
        try:
            logger.info(f"尝试登录，用户: {username}")
            
            # 填写登录表单
            with self.page.expect_navigation(wait_until="networkidle", timeout=self.timeout) as navigation_info:
                # 填写用户编号
                self.fill(self.NUMBER_INPUT, number)
                
                # 填写用户名
                self.fill(self.USERNAME_INPUT, username)
                
                # 填写密码
                self.fill(self.PASSWORD_INPUT, password)
                
                # 点击登录按钮
                self.click(self.LOGIN_BUTTON)
            
            # 等待导航完成
            navigation_info.value
            
            # 检查是否登录成功
            if self.page.locator(self.SUCCESS_MESSAGE).count() > 0:
                logger.info("登录成功")
                return True
            
            # 如果有错误消息，则登录失败
            if self.page.locator(self.ERROR_MESSAGE).count() > 0:
                error_message = self.get_error_message()
                logger.warning(f"登录失败: {error_message}")
                return False
            
            # 如果登录表单仍然存在，则登录失败
            if self.page.locator(self.LOGIN_FORM).count() > 0:
                logger.warning("登录失败: 登录表单仍然存在")
                return False
            
            # 默认认为登录成功
            logger.info("登录成功")
            return True
            
        except Exception as e:
            logger.error(f"登录过程中发生异常: {str(e)}")
            # 截图
            attach_screenshot(self.page, "login_error")
            return False
    
    def get_error_message(self):
        """获取错误消息
        
        Returns:
            str: 错误消息
        """
        try:
            error_element = self.page.locator(self.ERROR_MESSAGE)
            if error_element.count() > 0:
                return error_element.text_content()
            return ""
        except Exception as e:
            logger.error(f"获取错误消息失败: {str(e)}")
            return ""