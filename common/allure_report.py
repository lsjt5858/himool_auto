#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import allure
from datetime import datetime
from common.logger import logger

def attach_screenshot(page, name="screenshot"):
    """将截图附加到Allure报告
    
    Args:
        page: Playwright页面对象
        name: 截图名称
    """
    try:
        # 生成截图名称，包含时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{name}_{timestamp}"
        
        # 截图
        screenshot_bytes = page.screenshot()
        
        # 附加到Allure报告
        allure.attach(
            screenshot_bytes,
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )
        
        logger.info(f"截图已附加到报告: {screenshot_name}")
    except Exception as e:
        logger.error(f"截图失败: {str(e)}")

def attach_html(html, name="html"):
    """将HTML附加到Allure报告
    
    Args:
        html: HTML内容
        name: HTML名称
    """
    try:
        # 附加到Allure报告
        allure.attach(
            html,
            name=name,
            attachment_type=allure.attachment_type.HTML
        )
        
        logger.info(f"HTML已附加到报告: {name}")
    except Exception as e:
        logger.error(f"附加HTML失败: {str(e)}")

def attach_text(text, name="text"):
    """将文本附加到Allure报告
    
    Args:
        text: 文本内容
        name: 文本名称
    """
    try:
        # 附加到Allure报告
        allure.attach(
            text,
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"文本已附加到报告: {name}")
    except Exception as e:
        logger.error(f"附加文本失败: {str(e)}")