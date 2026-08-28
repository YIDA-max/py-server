"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-27 18:06:09
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-28 12:27:30
FilePath: \server-py\apps\web-service\app\core\middleware\response.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

import json

from fastapi import Request
from fastapi.responses import JSONResponse


async def unified_response(request: Request, call_next):
    # 前置处理
    # 执行功能
    response = await call_next(request)

    # 后置处理
    if not request.url.path.startswith("/api/"):
        return response

    body = b""
    async for chunk in response.body_iterator:
        body += chunk

    headers = dict(response.headers)
    headers.pop("content-length", None)

    data = json.loads(body) if body else None

    return JSONResponse(
        content={"code": "0", "data": data, "message": "success"},
        status_code=response.status_code,
        headers=headers,
    )


MIDDLEWARE = (unified_response, {})
