#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: API请求客户端封装

import json
import requests
from requests.exceptions import RequestException
from common.logger import get_logger


class ApiClient:
    """
    API请求客户端，封装requests库，提供统一的接口调用方式
    自动处理base_url拼接、请求/响应日志记录、异常处理等
    """
    
    def __init__(self, config, logger=None):
        """
        初始化API客户端
        :param config: 配置对象，包含base_url等配置信息
        :param logger: 日志记录器，如果不提供则创建新的logger
        """
        self.base_url = config.get('base_url', '')
        self.timeout = int(config.get('timeout', 10))
        self.retry_times = int(config.get('retry_times', 3))
        self.logger = logger or get_logger()
        self.session = requests.Session()
        
        # 如果配置中有token或api_key，可以设置为默认请求头
        self.default_headers = {}
        if config.get('api_key'):
            self.default_headers['X-API-Key'] = config.get('api_key')
        
        self.logger.info(f"API客户端初始化完成，base_url: {self.base_url}")
    
    def _build_url(self, endpoint):
        """
        构建完整的URL
        :param endpoint: API端点路径
        :return: 完整URL
        """
        # 确保base_url和endpoint之间只有一个'/'
        if self.base_url.endswith('/') and endpoint.startswith('/'):
            endpoint = endpoint[1:]
        elif not self.base_url.endswith('/') and not endpoint.startswith('/'):
            endpoint = '/' + endpoint
            
        return f"{self.base_url}{endpoint}"
    
    def _log_request(self, method, url, headers, data=None, params=None):
        """
        记录请求日志
        """
        self.logger.info(f"API请求: {method} {url}")
        self.logger.debug(f"请求头: {headers}")
        
        if params:
            self.logger.debug(f"查询参数: {params}")
        
        if data:
            # 避免日志中记录敏感信息
            log_data = data.copy() if isinstance(data, dict) else data
            if isinstance(log_data, dict) and 'password' in log_data:
                log_data['password'] = '******'
            self.logger.debug(f"请求体: {log_data}")
    
    def _log_response(self, response):
        """
        记录响应日志
        """
        self.logger.info(f"API响应: {response.status_code} {response.reason}")
        self.logger.debug(f"响应头: {response.headers}")
        
        try:
            # 尝试解析JSON响应
            response_json = response.json()
            self.logger.debug(f"响应体: {json.dumps(response_json, ensure_ascii=False)}")
        except ValueError:
            # 非JSON响应，记录文本内容
            if len(response.text) > 1000:
                self.logger.debug(f"响应体(截断): {response.text[:1000]}...")
            else:
                self.logger.debug(f"响应体: {response.text}")
    
    def request(self, method, endpoint, headers=None, params=None, data=None, json_data=None, **kwargs):
        """
        发送HTTP请求
        :param method: HTTP方法，如GET、POST等
        :param endpoint: API端点路径
        :param headers: 请求头
        :param params: URL查询参数
        :param data: 表单数据或字符串
        :param json_data: JSON数据
        :param kwargs: 其他requests支持的参数
        :return: 响应对象
        """
        url = self._build_url(endpoint)
        
        # 合并默认请求头和自定义请求头
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)
        
        # 记录请求日志
        self._log_request(method, url, request_headers, data, params)
        
        # 设置超时
        kwargs.setdefault('timeout', self.timeout)
        
        # 发送请求，支持重试
        response = None
        for attempt in range(self.retry_times):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    params=params,
                    data=data,
                    json=json_data,
                    **kwargs
                )
                break
            except RequestException as e:
                self.logger.error(f"请求异常: {e}")
                if attempt < self.retry_times - 1:
                    self.logger.info(f"重试请求 ({attempt + 1}/{self.retry_times})")
                else:
                    raise
        
        # 记录响应日志
        self._log_response(response)
        
        return response
    
    def get(self, endpoint, params=None, **kwargs):
        """
        发送GET请求
        :param endpoint: API端点路径
        :param params: URL查询参数
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        return self.request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint, data=None, json_data=None, **kwargs):
        """
        发送POST请求
        :param endpoint: API端点路径
        :param data: 表单数据
        :param json_data: JSON数据
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        return self.request('POST', endpoint, data=data, json_data=json_data, **kwargs)
    
    def put(self, endpoint, data=None, json_data=None, **kwargs):
        """
        发送PUT请求
        :param endpoint: API端点路径
        :param data: 表单数据
        :param json_data: JSON数据
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        return self.request('PUT', endpoint, data=data, json_data=json_data, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """
        发送DELETE请求
        :param endpoint: API端点路径
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        return self.request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint, data=None, json_data=None, **kwargs):
        """
        发送PATCH请求
        :param endpoint: API端点路径
        :param data: 表单数据
        :param json_data: JSON数据
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        return self.request('PATCH', endpoint, data=data, json_data=json_data, **kwargs)