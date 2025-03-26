#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from common.logger import logger
from common.page_objects.login_page import LoginPage
from common.data_utils import load_test_data
from config.settings import USERNAME, PASSWORD, USER_NUMBER

# 加载测试数据
test_data = load_test_data()
login_test_data = test_data.get('test_cases', {}).get('login', {})

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
        """测试使用有效凭据登录"""
        # 获取测试数据
        valid_data = login_test_data.get('valid', {})
        
        # 创建登录页面对象
        login_page = LoginPage(page)
        
        # 导航到登录页面
        with allure.step("导航到登录页面"):
            login_page.navigate()
        
        # 执行登录
        with allure.step("执行登录"):
            success = login_page.login(
                number=valid_data.get('number', USER_NUMBER),
                username=valid_data.get('username', USERNAME),
                password=valid_data.get('password', PASSWORD)
            )
        
        # 断言登录成功
        assert success, f"登录失败，错误信息: {login_page.get_error_message()}"
    
    @allure.story("登录功能")
    @allure.title("使用无效用户名登录")
    def test_login_with_invalid_username(self, page):
        """测试使用无效用户名登录"""
        # 获取测试数据
        invalid_data = login_test_data.get('invalid_username', {})
        
        # 创建登录页面对象
        login_page = LoginPage(page)
        
        # 导航到登录页面
        with allure.step("导航到登录页面"):
            login_page.navigate()
        
        # 执行登录
        with allure.step("执行登录"):
            success = login_page.login(
                number=invalid_data.get('number', USER_NUMBER),
                username=invalid_data.get('username', 'wrong_user'),
                password=invalid_data.get('password', PASSWORD)
            )
        
        # 断言登录失败
        assert not success, "登录应该失败但成功了"
        
    @allure.story("登录功能")
    @allure.title("使用无效密码登录")
    def test_login_with_invalid_password(self, page):
        """测试使用无效密码登录"""
        # 获取测试数据
        invalid_data = login_test_data.get('invalid_password', {})
        
        # 创建登录页面对象
        login_page = LoginPage(page)
        
        # 导航到登录页面
        with allure.step("导航到登录页面"):
            login_page.navigate()
        
        # 执行登录
        with allure.step("执行登录"):
            success = login_page.login(
                number=invalid_data.get('number', USER_NUMBER),
                username=invalid_data.get('username', USERNAME),
                password=invalid_data.get('password', 'wrong_password')
            )
        
        # 断言登录失败
        assert not success, "登录应该失败但成功了"