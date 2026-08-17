r"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-17 10:27:11
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-17 15:49:06
FilePath: \server-py\apps\web-service\app\model\category.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

# model/category.py
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# 导入多对多关联表（product 和 category 的中间表）
from app.model.association import product_category

# 导入基类 Base（ORM 基础）和 IDMixin（包含主键 id）
from app.model.base import Base, IDMixin

# TYPE_CHECKING：仅在类型检查工具（如 mypy、Pylance）运行时导入，避免循环导入
if TYPE_CHECKING:
    from app.model.product import Product


class Category(Base, IDMixin):
    """
    分类模型（商品分类）
    继承 Base（SQLAlchemy ORM 基类）和 IDMixin（自动包含 id 主键）

    对应数据库表名：默认为类名的小写复数形式，即 "categories"
    可通过 __tablename__ 自定义，但未定义时 SQLAlchemy 会自动生成
    """

    # ---------- 基础字段 ----------
    # 分类名称：必填（Mapped[str] 不含 None，自动推断为 NOT NULL）
    # 数据库类型 VARCHAR(50)，最大长度 50 个字符
    # 示例："电子产品"、"服装"、"食品"
    name: Mapped[str] = mapped_column(String(50))

    # 分类描述：长文本类型（TEXT），无长度限制
    # 默认值为空字符串（default=""），插入时如果不传则自动填入 ""
    # 注意：Mapped[str] 表示不允许为 NULL，但 default="" 保证了永远不会出现 NULL
    # 示例："包含手机、电脑、平板等电子产品"
    description: Mapped[str] = mapped_column(Text, default="")

    # ---------- 关联关系（多对多） ----------
    # 分类 ↔ 商品：多对多关系
    # 一个分类可以包含多个商品（如"电子产品"包含手机、电脑）
    # 一个商品也可以属于多个分类（如一款手机既属于"电子产品"也属于"热销品"）
    #
    # secondary=product_category：指定中间表，该表在 association.py 中定义
    #   - 中间表包含：category_id 和 product_id 两个外键
    # back_populates="categories"：与 Product 模型中的 categories 字段形成双向关系
    #   - 当通过 category.products 访问时，实际执行的是多对多关联查询
    #   - Product 模型中也有 categories: Mapped[list["Category"]] 对应
    #
    # 使用示例：
    #   category = await session.get(Category, 1)
    #   print(category.products)  # 获取该分类下的所有商品列表
    products: Mapped[list["Product"]] = relationship(
        secondary=product_category, back_populates="categories"
    )
