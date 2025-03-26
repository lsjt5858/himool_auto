#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
from locust import HttpUser, task, between

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.data_utils import load_test_data
from config.settings import BASE_URL

# 加载测试数据
test_data = load_test_data()
login_data = test_data.get('test_cases', {}).get('login', {}).get('valid', {})

class WebsiteUser(HttpUser):
    """模拟用户行为的压测类"""
    
    # 任务执行间隔时间（秒）
    wait_time = between(1, 3)
    
    # 主机地址
    host = BASE_URL
    
    def on_start(self):
        """用户启动时执行的操作"""
        self.login()
    
    def login(self):
        """用户登录"""
        login_url = "/user/login"
        payload = {
            "number": login_data.get('number', '001'),
            "username": login_data.get('username', 'admin'),
            "password": login_data.get('password', 'Lx123456')
        }
        
        with self.client.post(
            login_url,
            json=payload,
            catch_response=True,
            name="登录接口"
        ) as response:
            try:
                result = response.json()
                if result.get('code') == 0:
                    response.success()
                    # 保存token
                    self.token = result.get('data', {}).get('token')
                    if self.token:
                        self.client.headers.update({"Authorization": f"Bearer {self.token}"})
                else:
                    response.failure(f"登录失败: {result.get('message')}")
            except json.JSONDecodeError:
                response.failure("响应不是有效的JSON格式")
    
    @task(3)
    def get_user_info(self):
        """获取用户信息"""
        with self.client.get(
            "/user/info",
            catch_response=True,
            name="获取用户信息"
        ) as response:
            try:
                result = response.json()
                if result.get('code') == 0:
                    response.success()
                else:
                    response.failure(f"获取用户信息失败: {result.get('message')}")
            except json.JSONDecodeError:
                response.failure("响应不是有效的JSON格式")
    
    @task(1)
    def get_user_list(self):
        """获取用户列表"""
        with self.client.get(
            "/user/list",
            catch_response=True,
            name="获取用户列表"
        ) as response:
            try:
                result = response.json()
                if result.get('code') == 0:
                    response.success()
                else:
                    response.failure(f"获取用户列表失败: {result.get('message')}")
            except json.JSONDecodeError:
                response.failure("响应不是有效的JSON格式")