#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/3/27
# @Description: [对文件功能等的简要描述（可自行添加）]

import pytest,requests
import allure
from common.api_client import APIClient
from common.logger import get_logger
from common.data_utils import random_string

from common.api_client import APIClient


class Login():

    def login(self):
        url = "http://localhost:8080/api/user/get_token/"
        payload = {
            "number": "001",
            "username": "admin",
            "password": "Lx123456"
        }
        resp = requests.post(url, json=payload)
        print(resp.json())


        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.text)
            return None

if __name__ == '__main__':
    login = Login()
    login.login()