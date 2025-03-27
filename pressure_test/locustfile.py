from locust import HttpUser, task, between
from common.logger import get_logger
from common.data_utils import random_string, random_phone

logger = get_logger()

class WebsiteUser(HttpUser):
    """模拟用户行为的压测类"""
    
    # 任务执行间隔时间(秒)
    wait_time = between(1, 3)
    
    def on_start(self):
        """用户开始前的操作，例如登录"""
        logger.info("压测用户开始执行")
        self.login()
    
    def login(self):
        """登录操作"""
        response = self.client.post("/login", json={
            "username": "test_user",
            "password": "password123"
        })
        
        if response.status_code == 200:
            result = response.json()
            self.token = result.get("token")
            logger.info("压测用户登录成功")
            # 设置后续请求的公共头
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})
        else:
            logger.error(f"压测用户登录失败: {response.status_code} - {response.text}")
    
    @task(3)
    def get_user_info(self):
        """获取用户信息接口"""
        with self.client.get("/api/user/info", name="获取用户信息", catch_response=True) as response:
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    response.success()
                else:
                    response.failure(f"业务错误: {result}")
            else:
                response.failure(f"HTTP错误: {response.status_code}")
    
    @task(1)
    def create_user(self):
        """创建用户接口"""
        username = random_string(8)
        user_data = {
            "username": username,
            "phone": random_phone(),
            "email": f"{username}@example.com"
        }
        
        with self.client.post("/api/user/create", json=user_data, name="创建用户", catch_response=True) as response:
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    # 保存用户ID用于后续操作
                    self.user_id = result.get("data", {}).get("id")
                    response.success()
                else:
                    response.failure(f"业务错误: {result}")
            else:
                response.failure(f"HTTP错误: {response.status_code}")
    
    @task(1)
    def update_user(self):
        """更新用户接口"""
        # 检查是否有可用的用户ID
        if not hasattr(self, "user_id"):
            return
        
        update_data = {
            "id": self.user_id,
            "email": f"updated_{random_string(5)}@example.com"
        }
        
        with self.client.put("/api/user/update", json=update_data, name="更新用户", catch_response=True) as response:
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    response.success()
                else:
                    response.failure(f"业务错误: {result}")
            else:
                response.failure(f"HTTP错误: {response.status_code}")