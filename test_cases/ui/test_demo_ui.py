#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from common.logger import logger
from common.page_objects.login_page import LoginPage
from common.data_utils import load_test_data

@allure.epic("UI测试")
@allure.feature("登录功能")
class TestLoginUI:
    """登录UI测试类"""
    
    @allure.story("登录页面")
    @allure.title("验证登录页面标题")
    def test_login_page_title(self, page):
        """测试登录页面标题"""
        # 创建登录页面对象
        login_page = LoginPage(page)
        
        # 导航到登录页面
        with allure.step("导航到登录页面"):
            login_page.navigate()
        
        # 获取页面标题
        with allure.step("获取页面标题"):
            title = login_page.get_title()
        
        # 断言页面标题
        assert "登录" in title, f"页面标题 '{title}' 不包含 '登录'"
    
    @allure.story("登录功能")
    @allure.title("使用正确的凭据登录")
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, page):
        """测试使