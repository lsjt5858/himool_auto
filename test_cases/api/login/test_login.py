#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: 登录API测试用例

import pytest
import requests
import json
import allure

@allure.epic("API测试")
@allure.feature("用户管理")
class TestLogin:
    
    @allure.story("用户登录")
    @allure.title("测试登录接口")

    def test_login(self):
        """
        测试登录API接口
        """
        # 设置请求URL和参数
        url = "http://localhost:8080/api/user/get_token/"
        payload = {
            "number": "001",
            "password": "Lx123456",
            "username": "admin"
        }
        
        # 添加测试步骤
        with allure.step("发送登录请求"):
            allure.attach(json.dumps(payload, ensure_ascii=False, indent=2), 
                         "请求参数", allure.attachment_type.JSON)
            response = requests.post(url, json=payload)
        
        # 记录响应结果
        with allure.step("获取响应结果"):
            allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
            allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
        
        # 断言响应状态码
        with allure.step("验证响应状态码"):
            assert response.status_code == 200, f"登录失败，状态码: {response.status_code}"
        
        # 断言响应内容
        with allure.step("验证响应内容"):
            resp_data = response.json()
            assert "access" in resp_data, "响应中没有access token字段"
            assert "refresh" in resp_data, "响应中没有refresh token字段"
            assert resp_data.get("access"), "access token值为空"
            assert resp_data.get("refresh"), "refresh token值为空"

        # 输出token信息
        with allure.step("获取token信息"):
            access_token = resp_data.get("access")
            refresh_token = resp_data.get("refresh")
            allure.attach(access_token, "获取到的access token", allure.attachment_type.TEXT)
            allure.attach(refresh_token, "获取到的refresh token", allure.attachment_type.TEXT)
            
        return access_token

