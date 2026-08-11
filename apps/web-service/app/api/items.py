"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-11 20:04:31
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-11 20:05:17
FilePath: \server-py\apps\web-service\app\api\items.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from fastapi import APIRouter

from app.schema.item import Item

router = APIRouter(prefix="/items")


@router.get("/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
