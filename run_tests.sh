#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 创建日志和报告目录
mkdir -p logs
mkdir -p reports/html_report
mkdir -p reports/allure_results
mkdir -p reports/pressure_report

# 显示菜单
echo -e "${YELLOW}===== 自动化测试框架运行脚本 =====${NC}"
echo "1. 运行所有测试"
echo "2. 运行API测试"
echo "3. 运行UI测试"
echo "4. 运行冒烟测试"
echo "5. 运行压力测试"
echo "6. 生成Allure报告"
echo "7. 安装依赖"
echo "8. 安装Playwright浏览器"
echo "0. 退出"

# 读取用户输入
read -p "请选择操作 [0-8]: " choice

case $choice in
    1)
        echo -e "${GREEN}运行所有测试...${NC}"
        python -m pytest
        ;;
    2)
        echo -e "${GREEN}运行API测试...${NC}"
        python -m pytest test_cases/api/
        ;;
    3)
        echo -e "${GREEN}运行UI测试...${NC}"
        python -m pytest test_cases/ui/
        ;;
    4)
        echo -e "${GREEN}运行冒烟测试...${NC}"
        python -m pytest -m smoke
        ;;
    5)
        echo -e "${GREEN}运行压力测试...${NC}"
        echo "请在浏览器中访问 http://localhost:8089 查看压测结果"
        cd pressure_test && python -m locust -f locustfile.py
        ;;
    6)
        echo -e "${GREEN}生成Allure报告...${NC}"
        allure generate reports/allure_results -o reports/html_report --clean
        echo -e "${GREEN}报告生成完成，正在打开...${NC}"
        allure open reports/html_report
        ;;
    7)
        echo -e "${GREEN}安装依赖...${NC}"
        pip install -r requirements.txt
        ;;
    8)
        echo -e "${GREEN}安装Playwright浏览器...${NC}"
        python -m playwright install
        ;;
    0)
        echo -e "${GREEN}退出脚本${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}无效选择，请重新运行脚本${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}操作完成!${NC}"