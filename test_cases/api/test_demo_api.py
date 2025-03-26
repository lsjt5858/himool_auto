#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import allure
from common.logger import logger
from common.data_utils import load_test_data

# 加载测试数据
test_data = load_test_data()
login_test_data = test_data.get('test_cases', {}).get('login', {})

@allure.epic("API测试")
@allure.feature("用户管理")
class TestUserAPI:
    """用户API测试类"""
    
    @allure.story("登录接口")
    @allure.title("使用有效凭据登录")
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, api_client):
        """测试使用有效凭据登录"""
        # 获取测试数据
        valid_data = login_test_data.get('valid', {})
        
        # 发送登录请求
        with allure.step("发送登录请求"):
            response = api_client.login(
                number=valid_data.get('number'),
                username=valid_data.get('username'),
                password=valid_data.get('password')
            )
        
        # 断言响应
        with allure.step("验证登录成功"):
            assert response.get('code') == 0, f"登录失败: {response.get('message')}"
            assert 'data' in response, "响应中缺少data字段"
            assert 'token' in response.get('data', {}), "响应中缺少token字段"
    
    @allure.story("登录接口")
    @allure.title("使用无效用户名登录")
    def test_login_with_invalid_username(self, api_client):
        """测试使用无效用户名登录"""
        # 获取测试数据
        invalid_data = login_test_data.get('invalid_username', {})
        
        # 发送登录请求
        with allure.step("发送登录请求"):
            response = api_client.login(
                number=invalid_data.get('number'),
                username=invalid_data.get('username'),
                password=invalid_data.get('password')
            )
        
        # 断言响应
        with allure.step("验证登录失败"):
            assert response.get('code') != 0, "登录应该失败但成功了"
    
    @allure.story("登录接口")
    @allure.title("使用无效密码登录")
    def test_login_with_invalid_password(self, api_client):
        """测试使用无效密码登录"""
        # 获取测试数据
        invalid_data = login_test_data.get('invalid_password', {})
        
        # 发送登录请求
        with allure.step("发送登录请求"):
            response = api_client.login(
                number=invalid_data.get('number'),
                username=invalid_data.get('username'),
                password=invalid_data.get('password')
            )
        
        # 断言响应
        with allure.step("验证登录失败"):
            assert response.get('code') != 0, "登录应该失败但成功了"
    
    @allure.story("登录接口")
    @allure.title("使用空用户名登录")
    def test_login_with_empty_username(self, api_client):
        """测试使用空用户名登录"""
        # 获取测试数据
        invalid_data = login_test_data.get('empty_username', {})
        
        # 发送登录请求
        with allure.step("发送登录请求"):
            response = api_client.login(
                number=invalid_data.get('number'),
                username=invalid_data.get('username'),
                password=invalid_data.get('password')
            )
        
        # 断言响应
        with allure.step("验证登录失败"):
            assert response.get('code') != 0, "登录应该失败但成功了"
    
    @allure.story("登录接口")
    @allure.title("使用空密码登录")
    def test_login_with_empty_password(self, api_client):
        """测试使用空密码登录"""
        # 获取测试数据
        invalid_data = login_test_data.get('empty_password', {})
        
        # 发送登录请求
        with allure.step("发送登录请求"):
            response = api_client.login(
                number=invalid_data.get('number'),
                username=invalid_data.get('username'),
                password=invalid_data.get('password')
            )
        
        # 断言响应
        with allure.step("验证登录失败"):
            assert response.get('code') != 0, "登录应该失败但成功了"
    
    @allure.story("登录接口")
    @allure.title("登录后获取用户信息")
    @pytest.mark.dependency(depends=["test_login_with_valid_credentials"])
    def test_get_user_info_after_login(self, logged_in_api_client):
        """测试登录后获取用户信息"""
        # 获取用户信息
        with allure.step("获取用户信息"):
            response = logged_in_api_client.get("/user/info")
        
        # 断言响应
        with allure.step("验证用户信息"):
            assert response.get('code') == 0, f"获取用户信息失败: {response.get('message')}"
            assert 'data' in response, "响应中缺少data字段"
            user_data = response.get('data', {})
            assert 'username' in user_data, "用户信息中缺少username字段"
            assert user_data.get('username') == "admin", "用户名不匹配"