## 框架目录结构
```plaintext
project_root/
├── config/                   # 配置文件
│   ├── config.ini            # 全局配置文件（环境切换、参数等）
│   └── settings.py           # Python 动态配置（可选）
├── test_cases/               # 测试用例目录
│   ├── api/                  # API 测试用例
│   │   └── test_demo_api.py
│   └── ui/                   # UI 测试用例
│       └── test_demo_ui.py
├── common/                   # 公共模块
│   ├── api_client.py         # Requests 二次封装（带日志/鉴权）
│   ├── page_objects/         # Playwright 页面对象模型（POM）
│   │   └── base_page.py
│   ├── data_utils.py         # 测试数据生成工具
│   ├── logger.py             # 日志模块
│   └── allure_report.py      # Allure 报告定制（可选）
├── data/                     # 测试数据文件
│   └── test_data.json
├── pressure_test/            # 压测目录
│   └── locustfile.py         # Locust 压测脚本
├── reports/                  # 测试报告
│   ├── html_report/          # Pytest-HTML/Allure 报告
│   └── pressure_report/      # Locust 压测结果
├── logs/                     # 运行日志
├── conftest.py               # Pytest 全局 Fixture
├── pytest.ini                # Pytest 配置文件
├── requirements.txt          # 依赖库清单
└── README.md                 # 框架使用说明 