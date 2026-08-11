"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-11 20:04:25
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-11 20:04:52
FilePath: \server-py\apps\web-service\app\api\welcome.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Hello World", description="这是一个测试接口")
async def read_root():
    return {"Hello": "World"}
