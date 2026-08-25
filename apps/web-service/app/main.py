r"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-11 21:14:53
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-14 16:45:06
FilePath: \server-py\apps\web-service\app\main.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from fastapi import FastAPI
from app.core.config import common_settings, web_settings
from app.api.welcome import router as welcome_router


app = FastAPI(
    title=web_settings.app_name,
    docs_url=None if common_settings.environment == "production" else "/docs",
    redoc_url=None if common_settings.environment == "production" else "/redoc",
    openapi_url=(
        None if common_settings.environment == "production" else "/openapi.json"
    ),
)

# 注册欢迎路由
app.include_router(welcome_router)
