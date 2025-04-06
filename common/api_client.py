#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: API客户端，封装HTTP请求和认证

import requests
import json
from common.logger import get_logger


class ApiClient:
    """
    API客户端，封装HTTP请求和认证
    提供统一的接口调用方法，支持token认证
    """
    
    def __init__(self, base_url="http://localhost:8080", logger=None):
        """
        初始化API客户端
        :param base_url: API基础URL
        :param logger: 日志记录器，如果不提供则创建新的logger
        """
        self.base_url = base_url.rstrip('/')
        self.logger = logger or get_logger()
        self.access_token = None
        self.refresh_token = None
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def login(self, username="admin", password="Lx123456", number="001"):
        """
        登录并获取token
        :param username: 用户名
        :param password: 密码
        :param number: 编号
        :return: 登录响应数据
        """
        url = f"{self.base_url}/api/user/get_token/"
        payload = {
            "username": username,
            "password": password,
            "number": number
        }
        
        self.logger.info(f"登录系统: {url}")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            resp_data = response.json()
            self.access_token = resp_data.get("access")
            self.refresh_token = resp_data.get("refresh")
            
            if self.access_token:
                self.headers["Authorization"] = f"Bearer {self.access_token}"
                self.logger.info("登录成功，已获取token")
            else:
                self.logger.error("登录成功但未获取到token")
        else:
            self.logger.error(f"登录失败: {response.status_code} - {response.text}")
        
        return response
    
    def get(self, endpoint, params=None):
        """
        发送GET请求
        :param endpoint: API端点
        :param params: 请求参数
        :return: 响应对象
        """
        # 确保URL以斜杠结尾
        endpoint = endpoint.lstrip('/')
        if not endpoint.endswith('/'):
            endpoint = f"{endpoint}/"
        url = f"{self.base_url}/{endpoint}"
        self.logger.info(f"GET请求: {url}")
        
        response = requests.get(url, params=params, headers=self.headers)
        self._log_response(response)
        return response
    
    def post(self, endpoint, data=None, json_data=None):
        """
        发送POST请求
        :param endpoint: API端点
        :param data: 表单数据
        :param json_data: JSON数据
        :return: 响应对象
        """
        # 确保URL以斜杠结尾
        endpoint = endpoint.lstrip('/')
        if not endpoint.endswith('/'):
            endpoint = f"{endpoint}/"
        url = f"{self.base_url}/{endpoint}"
        self.logger.info(f"POST请求: {url}")
        
        response = requests.post(url, data=data, json=json_data, headers=self.headers)
        self._log_response(response)
        return response
    
    def put(self, endpoint, data=None, json_data=None):
        """
        发送PUT请求
        :param endpoint: API端点
        :param data: 表单数据
        :param json_data: JSON数据
        :return: 响应对象
        """
        # 确保URL以斜杠结尾
        endpoint = endpoint.lstrip('/')
        if not endpoint.endswith('/'):
            endpoint = f"{endpoint}/"
        url = f"{self.base_url}/{endpoint}"
        self.logger.info(f"PUT请求: {url}")
        
        response = requests.put(url, data=data, json=json_data, headers=self.headers)
        self._log_response(response)
        return response
    
    def delete(self, endpoint, params=None):
        """
        发送DELETE请求
        :param endpoint: API端点
        :param params: 请求参数
        :return: 响应对象
        """
        # 确保URL以斜杠结尾
        endpoint = endpoint.lstrip('/')
        if not endpoint.endswith('/'):
            endpoint = f"{endpoint}/"
        url = f"{self.base_url}/{endpoint}"
        self.logger.info(f"DELETE请求: {url}")
        
        response = requests.delete(url, params=params, headers=self.headers)
        self._log_response(response)
        return response
    
    def _log_response(self, response):
        """
        记录响应信息
        :param response: 响应对象
        """
        if response.status_code < 400:
            self.logger.info(f"响应状态码: {response.status_code}")
            self.logger.debug(f"响应内容: {response.text}")
        else:
            self.logger.error(f"请求失败: {response.status_code} - {response.text}")