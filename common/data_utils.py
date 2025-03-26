#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import random
import string
from datetime import datetime, timedelta
from faker import Faker
from common.logger import logger
from config.settings import DATA_DIR

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# 创建Faker实例
faker = Faker('zh_CN')

def load_test_data(file_name='test_data.json'):
    """加载测试数据
    
    Args:
        file_name: 数据文件名
        
    Returns:
        dict: 测试数据
    """
    file_path = os.path.join(DATA_DIR, file_name)
    
    if not os.path.exists(file_path):
        logger.warning(f"测试数据文件不存在: {file_path}")
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"加载测试数据: {file_path}")
        return data
    except Exception as e:
        logger.error(f"加载测试数据失败: {str(e)}")
        return {}

def save_test_data(data, file_name='test_data.json'):
    """保存测试数据
    
    Args:
        data: 测试数据
        file_name: 数据文件名
        
    Returns:
        bool: 是否保存成功
    """
    file_path = os.path.join(DATA_DIR, file_name)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"保存测试数据: {file_path}")
        return True
    except Exception as e:
        logger.error(f"保存测试数据失败: {str(e)}")
        return False

def generate_random_string(length=8):
    """生成随机字符串
    
    Args:
        length: 字符串长度
        
    Returns:
        str: 随机字符串
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_random_number(length=6):
    """生成随机数字
    
    Args:
        length: 数字长度
        
    Returns:
        str: 随机数字
    """
    return ''.join(random.choice(string.digits) for _ in range(length))

def generate_random_phone():
    """生成随机手机号
    
    Returns:
        str: 随机手机号
    """
    return faker.phone_number()

def generate_random_email():
    """生成随机邮箱
    
    Returns:
        str: 随机邮箱
    """
    return faker.email()

def generate_random_name():
    """生成随机姓名
    
    Returns:
        str: 随机姓名
    """
    return faker.name()

def generate_random_address():
    """生成随机地址
    
    Returns:
        str: 随机地址
    """
    return faker.address()

def generate_random_date(start_date=None, end_date=None):
    """生成随机日期
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        
    Returns:
        str: 随机日期，格式：YYYY-MM-DD
    """
    if not start_date:
        start_date = datetime.now() - timedelta(days=365)
    if not end_date:
        end_date = datetime.now()
    
    return faker.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')

def generate_test_user():
    """生成测试用户数据
    
    Returns:
        dict: 测试用户数据
    """
    return {
        'number': generate_random_number(3),
        'username': faker.user_name(),
        'password': 'Test' + generate_random_string(6),
        'name': generate_random_name(),
        'phone': generate_random_phone(),
        'email': generate_random_email(),
        'address': generate_random_address()
    }