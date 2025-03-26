#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# 加载测试数据
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
test_data_path = os.path.join(data_dir, 'test_data.json')
with open(test_data_path, 'r', encoding='utf-8') as f:
    TEST_DATA = json.load(f)

# 用户数据
USERS = TEST_DATA.get('users', [])

@app.route('/user/login', methods=['POST'])
def login():
    data = request.json
    number = data.get('number')
    username = data.get('username')
    password = data.get('password')
    
    # 验证用户凭据
    for user in USERS:
        if user.get('number') == number and user.get('username') == username and user.get('password') == password:
            return jsonify({
                'code': 0,
                'message': '登录成功',
                'data': {
                    'token': 'mock_token_123456',
                    'username': username,
                    'name': user.get('name'),
                    'role': user.get('role')
                }
            })
    
    return jsonify({
        'code': 1,
        'message': '用户名或密码错误',
        'data': None
    })

@app.route('/user/info', methods=['GET'])
def user_info():
    # 在实际应用中，这里应该验证token
    # 这里简化处理，直接返回admin用户信息
    for user in USERS:
        if user.get('username') == 'admin':
            return jsonify({
                'code': 0,
                'message': '获取用户信息成功',
                'data': {
                    'username': user.get('username'),
                    'name': user.get('name'),
                    'role': user.get('role')
                }
            })
    
    return jsonify({
        'code': 1,
        'message': '获取用户信息失败',
        'data': None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)