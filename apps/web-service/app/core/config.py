"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-27 18:06:09
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-31 10:36:25
FilePath: \server-py\apps\web-service\app\core\config.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from pydantic_settings import BaseSettings


class BaseSettingsWithEnv(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}


class CommonSettings(BaseSettingsWithEnv):
    environment: str = "development"


class WebSettings(BaseSettingsWithEnv):
    app_name: str = "Web Service API"  # 实际读取 WEB_APP_NAME
    cors_origins: str = ""  # 实际读取 WEB_CORS_ORIGINS，多个来源用逗号分隔
    cors_expose_headers: str = ""  # 实际读取 WEB_CORS_EXPOSE_HEADERS

    model_config = {"env_prefix": "WEB_"}


class DBSettings(BaseSettingsWithEnv):
    host: str = ""
    port: str = ""
    name: str = ""
    user: str = ""
    password: str = ""

    model_config = {"env_prefix": "DB_"}


common_settings = CommonSettings()
web_settings = WebSettings()
db_settings = DBSettings()
