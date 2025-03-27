import json
# from lib2to3.pgen2.token import NUMBER

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from common.logger import get_logger
from config.settings import BASE_URL, USERNAME, PASSWORD, REQUEST_TIMEOUT, MAX_RETRIES, NUMBER

logger = get_logger()



class APIClient:
    """API请求客户端封装"""
    
    def __init__(self, base_url=None, timeout=None):
        self.base_url = base_url or BASE_URL
        self.timeout = timeout or REQUEST_TIMEOUT
        self.session = requests.Session()
        self.token = None
        
        # 配置重试策略
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def login(self, username=None, password=None, number=None):
        """登录获取token"""
        username = username or USERNAME.strip('"')
        password = password or PASSWORD.strip('"')
        number = number or NUMBER.strip('"')
        
        # 使用正确的API路径
        url = f"{self.base_url}/api/user/get_token/"  # 修改为正确的API路径
        data = {
            "username": username,
            "password": password,
            "number": number
        }
        
        logger.info(f"登录请求: {url}")
        resp = requests.post(url, json=data)
        print(resp.json())
        response = self.session.post(url, json=data, timeout=self.timeout)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result.get("token")
            logger.info("登录成功，获取到token")
            return self.token
        else:
            logger.error(f"登录失败: {response.status_code} - {response.text}")
            return None
    
    def request(self, method, endpoint, params=None, data=None, json_data=None, headers=None, auth_required=True, **kwargs):
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        _headers = {}
        
        # 如果需要认证且token存在，添加到请求头
        if auth_required and self.token:
            _headers["Authorization"] = f"Bearer {self.token}"
        
        # 合并自定义请求头
        if headers:
            _headers.update(headers)
        
        # 记录请求信息
        logger.info(f"发送 {method.upper()} 请求: {url}")
        if params:
            logger.info(f"请求参数: {params}")
        if data:
            logger.info(f"表单数据: {data}")
        if json_data:
            logger.info(f"JSON数据: {json.dumps(json_data, ensure_ascii=False)}")
        
        # 发送请求
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json_data,
            headers=_headers,
            timeout=self.timeout,
            **kwargs
        )
        
        # 记录响应信息
        logger.info(f"响应状态码: {response.status_code}")
        try:
            response_data = response.json()
            logger.info(f"响应数据: {json.dumps(response_data, ensure_ascii=False)}")
        except:
            logger.info(f"响应内容: {response.text[:500]}...")
        
        return response
    
    def get(self, endpoint, params=None, **kwargs):
        """GET请求"""
        return self.request("get", endpoint, params=params, **kwargs)
    
    def post(self, endpoint, data=None, json_data=None, **kwargs):
        """POST请求"""
        return self.request("post", endpoint, data=data, json_data=json_data, **kwargs)
    
    def put(self, endpoint, data=None, json_data=None, **kwargs):
        """PUT请求"""
        return self.request("put", endpoint, data=data, json_data=json_data, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        """DELETE请求"""
        return self.request("delete", endpoint, **kwargs)

if __name__ == "__main__":
    api_client = APIClient()
    # 添加调试信息
    print("尝试登录...")
    token = api_client.login()
