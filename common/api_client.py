#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from requests.exceptions import RequestException
from common.logger import logger
from config.settings import BASE_URL, TIMEOUT

class APIClient:
    """API客户端
    
    封装HTTP请求，提供通用的API调用方法。
    """
    
    def __init__(self, base_url=None):
        """初始化API客户端
        
        Args:
            base_url: API基础URL，默认使用配置文件中的BASE_URL
        """
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()
        self.timeout = TIMEOUT
        self.token = None
    
    def login(self, number, username, password):
        """用户登录
        
        Args:
            number: 用户编号
            username: 用户名
            password: 密码
            
        Returns:
            dict: 登录响应数据
        """
        url = f"{self.base_url}/user/login"
        data = {
            "number": number,
            "username": username,
            "password": password
        }
        
        response = self.post(url, json=data)
        
        # 如果登录成功，保存token
        if response.get('code') == 0:
            self.token = response.get('data', {}).get('token')
            logger.info(f"登录成功，用户: {username}")
        else:
            logger.error(f"登录失败: {response.get('message')}")
        
        return response
    
    def logout(self):
        """用户登出
        
        Returns:
            dict: 登出响应数据
        """
        url = f"{self.base_url}/user/logout"
        response = self.post(url)
        
        # 清除token
        self.token = None
        logger.info("用户已登出")
        
        return response
    
    def get(self, url, params=None, **kwargs):
        """发送GET请求
        
        Args:
            url: 请求URL
            params: 查询参数
            **kwargs: 其他参数
            
        Returns:
            dict: 响应数据
        """
        return self._request('GET', url, params=params, **kwargs)
    
    def post(self, url, data=None, json=None, **kwargs):
        """发送POST请求
        
        Args:
            url: 请求URL
            data: 表单数据
            json: JSON数据
            **kwargs: 其他参数
            
        Returns:
            dict: 响应数据
        """
        return self._request('POST', url, data=data, json=json, **kwargs)
    
    def put(self, url, data=None, **kwargs):
        """发送PUT请求
        
        Args:
            url: 请求URL
            data: 请求数据
            **kwargs: 其他参数
            
        Returns:
            dict: 响应数据
        """
        return self._request('PUT', url, data=data, **kwargs)
    
    def delete(self, url, **kwargs):
        """发送DELETE请求
        
        Args:
            url: 请求URL
            **kwargs: 其他参数
            
        Returns:
            dict: 响应数据
        """
        return self._request('DELETE', url, **kwargs)
    
    def _request(self, method, url, **kwargs):
        """发送HTTP请求
        
        Args:
            method: 请求方法
            url: 请求URL
            **kwargs: 其他参数
            
        Returns:
            dict: 响应数据
        """
        # 如果URL不是完整的URL，则添加基础URL
        if not url.startswith(('http://', 'https://')):
            url = f"{self.base_url}{url}"
        
        # 设置超时
        kwargs.setdefault('timeout', self.timeout)
        
        # 如果有token，添加到请求头
        if self.token:
            headers = kwargs.get('headers', {})
            headers['Authorization'] = f"Bearer {self.token}"
            kwargs['headers'] = headers
        
        # 记录请求信息
        log_message = f"发送 {method} 请求: {url}"
        if kwargs.get('params'):
            log_message += f", params: {kwargs.get('params')}"
        if kwargs.get('data'):
            log_message += f", data: {kwargs.get('data')}"
        if kwargs.get('json'):
            log_message += f", json: {kwargs.get('json')}"
        logger.info(log_message)
        
        try:
            # 发送请求
            response = self.session.request(method, url, **kwargs)
            
            # 尝试解析JSON响应
            try:
                data = response.json()
            except ValueError:
                data = {'text': response.text}
            
            # 记录响应信息
            logger.info(f"收到响应: {response.status_code}, {data}")
            
            # 检查响应状态码
            response.raise_for_status()
            
            return data
        except RequestException as e:
            logger.error(f"请求异常: {str(e)}")
            return {'error': str(e)}