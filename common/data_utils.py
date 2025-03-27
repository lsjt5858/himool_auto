import json
import os
import random
import string
import time
from datetime import datetime, timedelta
import faker
from config.settings import BASE_DIR

# 创建faker实例
fake = faker.Faker('zh_CN')

def load_json_data(file_path):
    """加载JSON测试数据"""
    full_path = os.path.join(BASE_DIR, file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_data(data, file_path):
    """保存JSON测试数据"""
    full_path = os.path.join(BASE_DIR, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def random_string(length=10):
    """生成随机字符串"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def random_phone():
    """生成随机手机号"""
    return fake.phone_number()

def random_email():
    """生成随机邮箱"""
    return fake.email()

def random_name():
    """生成随机中文姓名"""
    return fake.name()

def random_address():
    """生成随机地址"""
    return fake.address()

def random_id_card():
    """生成随机身份证号"""
    return fake.ssn()

def random_date(start_date='-30d', end_date='today'):
    """生成随机日期"""
    return fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')

def random_datetime(start_date='-30d', end_date='today'):
    """生成随机日期时间"""
    return fake.date_time_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d %H:%M:%S')

def timestamp_to_datetime(timestamp):
    """时间戳转日期时间"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_timestamp(dt_str, format='%Y-%m-%d %H:%M:%S'):
    """日期时间转时间戳"""
    dt = datetime.strptime(dt_str, format)
    return int(dt.timestamp())

def get_current_timestamp():
    """获取当前时间戳"""
    return int(time.time())

def get_current_datetime(format='%Y-%m-%d %H:%M:%S'):
    """获取当前日期时间"""
    return datetime.now().strftime(format)

def get_current_date(format='%Y-%m-%d'):
    """获取当前日期"""
    return datetime.now().strftime(format)

def get_date_before_days(days, format='%Y-%m-%d'):
    """获取几天前的日期"""
    return (datetime.now() - timedelta(days=days)).strftime(format)

def get_date_after_days(days, format='%Y-%m-%d'):
    """获取几天后的日期"""
    return (datetime.now() + timedelta(days=days)).strftime(format)