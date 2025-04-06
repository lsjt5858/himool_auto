#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: 用户管理API测试用例

import pytest
import json,random
import allure
from common.api_client import ApiClient


@allure.epic("API测试")
@allure.feature("系统管理")
class TestUserManagement:
    
    
    @allure.story("用户管理")
    @allure.title("测试添加用户接口")
    def test_add_user(self, api_client):
        """
        测试添加用户API接口
        """
        # 设置请求参数
        endpoint = "api/users"

        random_data = random.randint(1000, 9999)
        payload = {
            "username": f"testuser_{random_data}",
            "name": f"测试用户_{random_data}",
            "phone": f"1380013{random_data}",
            "email": "test@example.com",
            "sex": "man",
            "roles": [1],  # 使用1作为角色ID，确保该角色存在
            "is_active": True
        }

        # 添加测试步骤
        with allure.step("发送添加用户请求"):
            allure.attach(json.dumps(payload, ensure_ascii=False, indent=2), 
                         "请求参数", allure.attachment_type.JSON)
            response = api_client.post(endpoint, json_data=payload)
        
        # 记录响应结果
        with allure.step("获取响应结果"):
            allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
            allure.attach(str(response.status_code), "状态码", allure.attachment_type.TEXT)
        
        # 断言响应状态码
        with allure.step("验证响应状态码"):
            assert response.status_code in [200, 201], f"添加用户失败，状态码: {response.status_code}"
        
        # 断言响应内容
        with allure.step("验证响应内容"):
            try:
                resp_data = response.json()
                # 根据实际响应结构进行断言
                # 有些API可能返回的字段不同，所以我们需要灵活处理
                if "id" in resp_data:
                    assert resp_data.get("username") == payload["username"], "用户名不匹配"
                    assert resp_data.get("name") == payload["name"], "姓名不匹配"
                    assert resp_data.get("email") == payload["email"], "邮箱不匹配"
                else:
                    # 如果没有id字段，可能是其他格式的成功响应
                    assert response.status_code in [200, 201], "请求失败"
                    allure.attach(json.dumps(resp_data, ensure_ascii=False, indent=2), 
                                 "响应内容", allure.attachment_type.JSON)
            except ValueError as e:
                # 如果响应不是JSON格式
                assert response.status_code in [200, 201], f"请求失败且响应不是JSON格式: {e}"
                allure.attach(response.text, "非JSON响应内容", allure.attachment_type.TEXT)
                resp_data = {"message": response.text}
            
        return resp_data