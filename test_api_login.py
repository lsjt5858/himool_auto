import sys
import time
from common.api_client import APIClient
from common.logger import get_logger

logger = get_logger()

def test_login_endpoints():
    # 测试不同的API端点
    endpoints = [
        "/api/login",
        "/api/v1/login",
        "/login",
        "/user/login",
        "/api/user/login"
    ]
    
    base_url = "http://localhost:8080"
    
    for endpoint in endpoints:
        print(f"\n测试登录端点: {endpoint}")
        # 创建一个新的API客户端实例
        client = APIClient(base_url=base_url)
        
        # 保存原始方法
        original_login = client.login
        
        # 重写登录方法以使用自定义URL
        def custom_login(username=None, password=None, number=None):
            url = f"{base_url}{endpoint}"
            username = username or "admin"
            password = password or "Lx123456"
            number = number or "001"
            
            data = {
                "username": username,
                "password": password,
                "number": number
            }
            
            logger.info(f"登录请求: {url}")
            response = client.session.post(url, json=data, timeout=client.timeout)
            
            if response.status_code == 200:
                result = response.json()
                client.token = result.get("token")
                logger.info("登录成功，获取到token")
                return client.token
            else:
                logger.error(f"登录失败: {response.status_code} - {response.text}")
                return None
                
        # 替换登录方法
        client.login = custom_login
        
        # 尝试登录
        try:
            token = client.login(username="admin", password="Lx123456", number="001")
            if token:
                print(f"✅ 登录成功! 端点 {endpoint} 有效")
                return endpoint
            else:
                print(f"❌ 登录失败: 端点 {endpoint} 无效")
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
        
        # 等待一秒再尝试下一个端点
        time.sleep(1)
    
    return None

if __name__ == "__main__":
    print("开始测试API登录端点...")
    valid_endpoint = test_login_endpoints()
    
    if valid_endpoint:
        print(f"\n找到有效的登录端点: {valid_endpoint}")
        print("请更新 api_client.py 中的登录URL为此端点")
    else:
        print("\n未找到有效的登录端点，请检查服务器是否正常运行或API路径是否正确")