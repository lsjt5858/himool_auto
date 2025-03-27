import pytest
import allure
from common.api_client import APIClient
from common.logger import get_logger
from common.data_utils import random_string, random_phone

logger = get_logger()

@allure.epic("API测试")
@allure.feature("示例API")
class TestDemoAPI:
    
    @pytest.fixture(scope="class")
    def api_client(self):
        """API客户端"""
        client = APIClient()
        client.login()  # 登录获取token
        return client
    
    @allure.story("获取用户信息")
    @allure.title("获取当前用户信息")
    def test_get_user_info(self, api_client):
        """测试获取用户信息接口"""
        with allure.step("发送获取用户信息请求"):
            response = api_client.get("/api/user/info")
        
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应数据"):
            data = response.json()
            assert data["code"] == 0
            assert "data" in data
            assert "username" in data["data"]
    
    @allure.story("创建用户")
    @allure.title("创建新用户")
    @pytest.mark.parametrize("username,phone", [
        (random_string(8), random_phone()),
        (random_string(10), random_phone())
    ])
    def test_create_user(self, api_client, username, phone):
        """测试创建用户接口"""
        user_data = {
            "username": username,
            "phone": phone,
            "email": f"{username}@example.com"
        }
        
        with allure.step(f"发送创建用户请求: {user_data}"):
            response = api_client.post("/api/user/create", json_data=user_data)
        
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应数据"):
            data = response.json()
            assert data["code"] == 0
            assert "data" in data
            assert "id" in data["data"]
            assert data["data"]["username"] == username
    
    @allure.story("更新用户")
    @allure.title("更新用户信息")
    def test_update_user(self, api_client):
        """测试更新用户接口"""
        # 先创建用户
        username = random_string(8)
        user_data = {
            "username": username,
            "phone": random_phone(),
            "email": f"{username}@example.com"
        }
        
        with allure.step(f"先创建用户: {user_data}"):
            create_response = api_client.post("/api/user/create", json_data=user_data)
            assert create_response.status_code == 200
            user_id = create_response.json()["data"]["id"]
        
        # 更新用户信息
        update_data = {
            "id": user_id,
            "email": f"updated_{username}@example.com"
        }
        
        with allure.step(f"发送更新用户请求: {update_data}"):
            response = api_client.put("/api/user/update", json_data=update_data)
        
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应数据"):
            data = response.json()
            assert data["code"] == 0
    
    @allure.story("删除用户")
    @allure.title("删除用户")
    def test_delete_user(self, api_client):
        """测试删除用户接口"""
        # 先创建用户
        username = random_string(8)
        user_data = {
            "username": username,
            "phone": random_phone(),
            "email": f"{username}@example.com"
        }
        
        with allure.step(f"先创建用户: {user_data}"):
            create_response = api_client.post("/api/user/create", json_data=user_data)
            assert create_response.status_code == 200
            user_id = create_response.json()["data"]["id"]
        
        # 删除用户
        with allure.step(f"发送删除用户请求: {user_id}"):
            response = api_client.delete(f"/api/user/delete/{user_id}")
        
        with allure.step("验证响应状态码"):
            assert response.status_code == 200
        
        with allure.step("验证响应数据"):
            data = response.json()
            assert data["code"] == 0