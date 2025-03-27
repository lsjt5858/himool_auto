
import pytest
import allure
from playwright.sync_api import expect
from common.logger import get_logger
from common.page_objects.base_page import BasePage
from common.allure_report import attach_screenshot

logger = get_logger()

class LoginPage(BasePage):
    """登录页面对象"""
    
    def __init__(self, page):
        super().__init__(page)
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.error_message = ".error-message"
    
    def navigate_to_login(self):
        """导航到登录页"""
        return self.navigate("/login")
    
    def login(self, username, password):
        """执行登录操作"""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
        return self
    
    def get_error_message(self):
        """获取错误信息"""
        return self.get_text(self.error_message)

class HomePage(BasePage):
    """首页页面对象"""
    
    def __init__(self, page):
        super().__init__(page)
        self.welcome_message = ".welcome-message"
        self.logout_button = "#logout"
    
    def get_welcome_message(self):
        """获取欢迎信息"""
        return self.get_text(self.welcome_message)
    
    def logout(self):
        """退出登录"""
        self.click(self.logout_button)
        return self

@allure.epic("UI测试")
@allure.feature("登录功能")
class TestLogin:
    
    @pytest.fixture(scope="function")
    def login_page(self, page):
        """登录页面对象"""
        return LoginPage(page)
    
    @pytest.fixture(scope="function")
    def home_page(self, page):
        """首页页面对象"""
        return HomePage(page)
    
    @allure.story("登录成功")
    @allure.title("使用有效凭据登录")
    def test_login_success(self, login_page, home_page):
        """测试登录成功"""
        with allure.step("导航到登录页"):
            login_page.navigate_to_login()
            attach_screenshot(login_page.page, "登录页面")
        
        with allure.step("输入用户名和密码并点击登录"):
            login_page.login("test_user", "password123")
        
        with allure.step("验证登录成功"):
            # 等待跳转到首页
            login_page.page.wait_for_url("**/home")
            attach_screenshot(login_page.page, "登录成功后页面")
            
            # 验证欢迎信息
            welcome_text = home_page.get_welcome_message()
            assert "欢迎" in welcome_text
    
    @allure.story("登录失败")
    @allure.title("使用无效凭据登录")
    @pytest.mark.parametrize("username,password,expected_error", [
        ("invalid_user", "password123", "用户名不存在"),
        ("test_user", "wrong_password", "密码错误"),
        ("", "password123", "请输入用户名"),
        ("test_user", "", "请输入密码")
    ])
    def test_login_failure(self, login_page, username, password, expected_error):
        """测试登录失败"""
        with allure.step("导航到登录页"):
            login_page.navigate_to_login()
        
        with allure.step(f"使用无效凭据登录: {username}/{password}"):
            login_page