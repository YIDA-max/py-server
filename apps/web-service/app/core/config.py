r"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-11 21:14:53
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-14 16:48:20
FilePath: \server-py\apps\web-service\app\core\config.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from pydantic_settings import BaseSettings


class _BaseSettingsWithEnv(BaseSettings):
    # 配置读取方式：加载 .env 文件，并忽略未定义的额外字段
    # 他会合并
    model_config = {"env_file": ".env", "extra": "ignore"}


# 通用配置
class _CommonSettings(_BaseSettingsWithEnv):
    environment: str = "development"


# web服务配置
class _WebSettings(_BaseSettingsWithEnv):
    app_name: str = "Web Service API"
    model_config = {"env_prefix": "WEB_"}


# 数据库配置
class _DBSettings(_BaseSettingsWithEnv):
    host: str = ""
    port: str = ""
    name: str = ""
    user: str = ""
    password: str = ""
    model_config = {"env_prefix": "DB_"}


common_settings = _CommonSettings()
web_settings = _WebSettings()
db_settings = _DBSettings()
