#!/bin/bash

# 设置项目根目录到PYTHONPATH环境变量
export PYTHONPATH=/Users/Apple/PycharmProjects/himool_auto_case

# 激活虚拟环境（使用绝对路径）
source /Users/Apple/PycharmProjects/himool_auto_case/nut_venv/bin/activate

# 运行测试用例（使用python3命令）
python3 -m pytest test_cases/api/test_demo_api.py -v

# 或者运行单个测试文件
# python3 -m pytest test_cases/api/test_demo_api.py