"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-17 10:28:16
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-17 10:28:24
FilePath: \server-py\apps\web-service\app\model\association\product_category.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from sqlalchemy import Column, ForeignKey, Table

from app.model.base import Base

product_category = Table(
    "product_category",
    Base.metadata,
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("category_id", ForeignKey("category.id"), primary_key=True),
)
