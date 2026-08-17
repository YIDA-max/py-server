"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-17 10:27:34
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-17 10:27:42
FilePath: \server-py\apps\web-service\app\model\product.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

# model/product.py
# model/product.py
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# 导入关联表（多对多中间表）
from app.model.association import product_category

# 导入基类（含 id 和审计字段）
from app.model.base import Base, IDMixin, TimestampMixin

# TYPE_CHECKING 避免循环导入，仅在类型检查时导入
if TYPE_CHECKING:
    from app.model.category import Category
    from app.model.sku import Sku


class Product(Base, IDMixin, TimestampMixin):
    """
    商品模型
    继承 Base（ORM 基类）、IDMixin（主键 id）、TimestampMixin（创建/更新时间）
    """

    # ---------- 基础字段 ----------
    # 商品名称：必填，VARCHAR(200)
    name: Mapped[str] = mapped_column(String(200))

    # 商品描述：长文本（TEXT），数据库默认空字符串，不允许 NULL
    description: Mapped[str] = mapped_column(Text, default="")

    # 品牌：可选字段（可为 NULL），VARCHAR(100)
    # 类型注解 str | None 会让 SQLAlchemy 自动推断 nullable=True
    brand: Mapped[str | None] = mapped_column(String(100))

    # ---------- 关联关系 ----------
    # 多对多：商品 ↔ 分类（通过 product_category 中间表）
    # back_populates 与 Category.products 形成双向关系
    categories: Mapped[list["Category"]] = relationship(
        secondary=product_category, back_populates="products"
    )

    # 一对多：商品 → SKU（一个商品有多个 SKU）
    # back_populates 与 Sku.product 形成双向关系
    skus: Mapped[list["Sku"]] = relationship(back_populates="product")
