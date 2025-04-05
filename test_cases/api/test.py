#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/3/29
# @Description: [对文件功能等的简要描述（可自行添加）]
import random

from common.data_utils import random_name
from datetime import datetime


name = "test_user_" + random_name()+datetime.now().strftime("_%Y%m%d%H%M%S")
print(name)

sex = random.choice(["man", "woman"])
print(sex)

