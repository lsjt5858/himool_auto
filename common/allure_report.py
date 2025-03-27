import os
import allure
import json
from datetime import datetime
from config.settings import ALLURE_RESULT_PATH

def attach_text(name, content):
    """添加文本附件"""
    allure.attach(
        body=content,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )

def attach_json(name, content):
    """添加JSON附件"""
    if isinstance(content, (dict, list)):
        content = json.dumps(content, ensure_ascii=False, indent=2)
    allure.attach(
        body=content,
        name=name,
        attachment_type=allure.attachment_type.JSON
    )

def attach_html(name, content):
    """添加HTML附件"""
    allure.attach(
        body=content,
        name=name,
        attachment_type=allure.attachment_type.HTML
    )

def attach_image(name, file_path=None, content=None):
    """添加图片附件"""
    if file_path:
        with open(file_path, 'rb') as f:
            content = f.read()
    
    if content:
        allure.attach(
            body=content,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

def attach_screenshot(page, name=None):
    """添加截图附件"""
    if name is None:
        name = f"screenshot_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    screenshot = page.screenshot()
    allure.attach(
        body=screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )

def attach_request_response(request_data, response_data, request_headers=None, response_headers=None):
    """添加请求响应附件"""
    # 请求数据
    if isinstance(request_data, (dict, list)):
        request_data = json.dumps(request_data, ensure_ascii=False, indent=2)
    attach_text("Request Data", request_data)
    
    # 请求头
    if request_headers:
        if isinstance(request_headers, dict):
            request_headers = json.dumps(request_headers, ensure_ascii=False, indent=2)
        attach_text("Request Headers", request_headers)
    
    # 响应数据
    if isinstance(response_data, (dict, list)):
        response_data = json.dumps(response_data, ensure_ascii=False, indent=2)
    attach_text("Response Data", response_data)
    
    # 响应头
    if response_headers:
        if isinstance(response_headers, dict):
            response_headers = json.dumps(response_headers, ensure_ascii=False, indent=2)
        attach_text("Response Headers", response_headers)

def set_allure_environment():
    """设置Allure环境变量"""
    from config.settings import CURRENT_ENV, BASE_URL, UI_URL
    
    env_data = {
        "Environment": CURRENT_ENV,
        "API URL": BASE_URL,
        "UI URL": UI_URL,
        "Python Version": os.popen("python --version").read().strip(),
        "Pytest Version": os.popen("pytest --version").read().strip(),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 确保目录存在
    os.makedirs(ALLURE_RESULT_PATH, exist_ok=True)
    
    # 写入环境文件
    with open(os.path.join(ALLURE_RESULT_PATH, "environment.properties"), "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")