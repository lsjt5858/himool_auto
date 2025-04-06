#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: 页面对象基类，封装Playwright基础操作

import time
from typing import Optional, Any, List, Dict, Union
from playwright.sync_api import Page, Locator, expect
from common.logger import get_logger


class BasePage:
    """
    页面对象基类，封装Playwright的基础操作
    提供统一的页面交互方法，集成日志记录
    """
    
    def __init__(self, page: Page, logger=None):
        """
        初始化页面对象
        :param page: Playwright的Page对象
        :param logger: 日志记录器，如果不提供则创建新的logger
        """
        self.page = page
        self.logger = logger or get_logger()
        self.logger.info(f"初始化页面对象: {self.__class__.__name__}")
    
    def goto(self, url: str, wait_until: str = 'load', timeout: int = 30000) -> None:
        """
        导航到指定URL
        :param url: 目标URL
        :param wait_until: 等待页面加载的条件，可选值: 'load', 'domcontentloaded', 'networkidle', 'commit'
        :param timeout: 超时时间(毫秒)
        """
        self.logger.info(f"导航到: {url}")
        self.page.goto(url, wait_until=wait_until, timeout=timeout)
    
    def get_locator(self, selector: str, has_text: str = None) -> Locator:
        """
        获取元素定位器
        :param selector: CSS选择器或XPath
        :param has_text: 包含的文本内容
        :return: Locator对象
        """
        if has_text:
            return self.page.locator(selector).filter(has_text=has_text)
        return self.page.locator(selector)
    
    def find_element(self, selector: str, has_text: str = None) -> Locator:
        """
        查找元素
        :param selector: CSS选择器或XPath
        :param has_text: 包含的文本内容
        :return: Locator对象
        """
        self.logger.debug(f"查找元素: {selector}")
        return self.get_locator(selector, has_text)
    
    def find_elements(self, selector: str) -> Locator:
        """
        查找多个元素
        :param selector: CSS选择器或XPath
        :return: Locator对象(可迭代)
        """
        self.logger.debug(f"查找多个元素: {selector}")
        return self.page.locator(selector)
    
    def click(self, selector: str, has_text: str = None, timeout: int = 5000, force: bool = False) -> None:
        """
        点击元素
        :param selector: CSS选择器或XPath
        :param has_text: 包含的文本内容
        :param timeout: 超时时间(毫秒)
        :param force: 是否强制点击
        """
        self.logger.info(f"点击元素: {selector}")
        element = self.find_element(selector, has_text)
        element.click(timeout=timeout, force=force)
    
    def fill(self, selector: str, value: str, timeout: int = 5000) -> None:
        """
        填充输入框
        :param selector: CSS选择器或XPath
        :param value: 要输入的值
        :param timeout: 超时时间(毫秒)
        """
        self.logger.info(f"填充输入框 {selector}: {value}")
        element = self.find_element(selector)
        element.fill(value, timeout=timeout)
    
    def type(self, selector: str, text: str, delay: int = 100) -> None:
        """
        模拟键盘输入
        :param selector: CSS选择器或XPath
        :param text: 要输入的文本
        :param delay: 输入延迟(毫秒)
        """
        self.logger.info(f"键盘输入 {selector}: {text}")
        element = self.find_element(selector)
        element.type(text, delay=delay)
    
    def select_option(self, selector: str, value: str = None, label: str = None, index: int = None) -> List[str]:
        """
        选择下拉选项
        :param selector: CSS选择器或XPath
        :param value: 选项的value属性
        :param label: 选项的文本内容
        :param index: 选项的索引
        :return: 已选择的选项值列表
        """
        self.logger.info(f"选择下拉选项 {selector}: value={value}, label={label}, index={index}")
        element = self.find_element(selector)
        
        if value is not None:
            return element.select_option(value=value)
        elif label is not None:
            return element.select_option(label=label)
        elif index is not None:
            return element.select_option(index=index)
        else:
            raise ValueError("必须提供value、label或index中的一个参数")
    
    def check(self, selector: str, force: bool = False) -> None:
        """
        选中复选框
        :param selector: CSS选择器或XPath
        :param force: 是否强制选中
        """
        self.logger.info(f"选中复选框: {selector}")
        element = self.find_element(selector)
        element.check(force=force)
    
    def uncheck(self, selector: str, force: bool = False) -> None:
        """
        取消选中复选框
        :param selector: CSS选择器或XPath
        :param force: 是否强制取消选中
        """
        self.logger.info(f"取消选中复选框: {selector}")
        element = self.find_element(selector)
        element.uncheck(force=force)
    
    def get_text(self, selector: str) -> str:
        """
        获取元素文本
        :param selector: CSS选择器或XPath
        :return: 元素文本内容
        """
        self.logger.debug(f"获取元素文本: {selector}")
        return self.find_element(selector).text_content()
    
    def get_attribute(self, selector: str, name: str) -> Optional[str]:
        """
        获取元素属性
        :param selector: CSS选择器或XPath
        :param name: 属性名
        :return: 属性值
        """
        self.logger.debug(f"获取元素属性 {selector}.{name}")
        return self.find_element(selector).get_attribute(name)
    
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        判断元素是否可见
        :param selector: CSS选择器或XPath
        :param timeout: 超时时间(毫秒)
        :return: 元素是否可见
        """
        self.logger.debug(f"判断元素是否可见: {selector}")
        try:
            self.find_element(selector).wait_for(state='visible', timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_selector(self, selector: str, state: str = 'visible', timeout: int = 5000) -> Locator:
        """
        等待元素出现
        :param selector: CSS选择器或XPath
        :param state: 等待的状态，可选值: 'attached', 'detached', 'visible', 'hidden'
        :param timeout: 超时时间(毫秒)
        :return: Locator对象
        """
        self.logger.info(f"等待元素 {selector} 状态: {state}")
        element = self.find_element(selector)
        element.wait_for(state=state, timeout=timeout)
        return element
    
    def wait_for_navigation(self, url: str = None, wait_until: str = 'load', timeout: int = 30000) -> None:
        """
        等待页面导航完成
        :param url: 期望导航到的URL，支持正则表达式
        :param wait_until: 等待页面加载的条件
        :param timeout: 超时时间(毫秒)
        """
        self.logger.info("等待页面导航完成")
        with self.page.expect_navigation(url=url, wait_until=wait_until, timeout=timeout):
            pass
    
    def wait_for_load_state(self, state: str = 'load', timeout: int = 30000) -> None:
        """
        等待页面加载状态
        :param state: 加载状态，可选值: 'load', 'domcontentloaded', 'networkidle'
        :param timeout: 超时时间(毫秒)
        """
        self.logger.info(f"等待页面加载状态: {state}")
        self.page.wait_for_load_state(state, timeout=timeout)
    
    def wait_for_timeout(self, timeout: int) -> None:
        """
        等待指定时间
        :param timeout: 等待时间(毫秒)
        """
        self.logger.debug(f"等待 {timeout} 毫秒")
        self.page.wait_for_timeout(timeout)
    
    def take_screenshot(self, path: str = None, full_page: bool = True) -> bytes:
        """
        截取页面截图
        :param path: 保存路径，如果不提供则返回截图数据
        :param full_page: 是否截取整个页面
        :return: 截图数据
        """
        self.logger.info(f"截取页面截图: {path if path else '(不保存)'}")
        return self.page.screenshot(path=path, full_page=full_page)
    
    def expect_element(self, selector: str, state: str = 'visible', timeout: int = 5000) -> None:
        """
        断言元素状态
        :param selector: CSS选择器或XPath
        :param state: 期望的状态，可选值: 'attached', 'detached', 'visible', 'hidden'
        :param timeout: 超时时间(毫秒)
        """
        self.logger.info(f"断言元素 {selector} 状态: {state}")
        element = self.find_element(selector)
        if state == 'visible':
            expect(element).to_be_visible(timeout=timeout)
        elif state == 'hidden':
            expect(element).to_be_hidden(timeout=timeout)
        elif state == 'attached':
            expect(element).to_be_attached(timeout=timeout)
        elif state == 'detached':
            expect(element).to_be_detached(timeout=timeout)
        else:
            raise ValueError(f"不支持的状态: {state}")
    
    def expect_text(self, selector: str, text: str, timeout: int = 5000) -> None:
        """
        断言元素文本内容
        :param selector: CSS选择器或XPath
        :param text: 期望的文本内容
        :param timeout: 超时时间(毫秒)
        """
        self.logger.info(f"断言元素 {selector} 文本内容: {text}")
        element = self.find_element(selector)
        expect(element).to_have_text(text, timeout=timeout)
    
    def reload(self, wait_until: str = 'load', timeout: int = 30000) -> None:
        """
        重新加载页面
        :param wait_until: 等待页面加载的条件
        :param timeout: 超时时间(毫秒)
        """
        self.logger.info("重新加载页面")
        self.page.reload(wait_until=wait_until, timeout=timeout)