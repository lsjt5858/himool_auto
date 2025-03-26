#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 尝试导入common模块
try:
    from common.page_objects.login_page import LoginPage
    print('导入成功!')
except ImportError as e:
    print(f'导入失败: {e}')