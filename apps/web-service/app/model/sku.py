"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-17 10:27:47
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-17 10:27:58
FilePath: \server-py\apps\web-service\app\model\sku.py
Description: SKU（库存量单位）数据模型，对应数据库中的 sku 表。

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

# model/sku.py
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.model.base import Base, IDMixin

if TYPE_CHECKING:
    from app.model.product import Product


class Sku(Base, IDMixin):
    """
    SKU 模型类，对应数据库中的 `sku` 表。
    用于存储商品的具体规格库存单元信息（如颜色、尺寸、价格、库存等）。
    """

    # ---------- 字段定义 ----------

    # 外键：关联到 product 表的主键 id
    # ondelete="CASCADE" 表示当对应的商品被删除时，该商品下的所有 SKU 也会自动被级联删除
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE"),
        comment="关联的商品ID（外键，级联删除）",
    )

    # SKU 编码，全局唯一，用于标识具体的规格组合
    # 长度限制 50 字符，并设置了唯一约束
    sku_code: Mapped[str] = mapped_column(
        String(50), unique=True, comment="SKU唯一编码，如 'iPhone15-512GB-黑色'"
    )

    # 价格，使用 Decimal 类型保证精度，总共 10 位数字，其中小数部分 2 位
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), comment="销售价格，单位：元，保留两位小数"
    )

    # 库存数量，默认为 0
    stock: Mapped[int] = mapped_column(default=0, comment="当前库存数量")

    # 属性字典，使用 PostgreSQL 的 JSONB 类型存储，可高效查询
    # 例如：{"颜色": "黑色", "尺寸": "XL", "材质": "棉"}
    attrs: Mapped[dict] = mapped_column(
        JSONB, comment="SKU 的属性键值对，如颜色、尺寸、版本等，使用 JSONB 存储"
    )

    # 图片 URL，存储该 SKU 对应的展示图片地址
    image_url: Mapped[str] = mapped_column(String, comment="SKU 的展示图片链接")

    # 喜好度，默认为 0
    preference: Mapped[int] = mapped_column(default=0, comment="喜好度，默认为 0")

    # ---------- 关系定义 ----------

    # 与 Product 模型的父子关系（反向引用）
    # product 属性会被自动填充为对应的 Product 实例
    # back_populates="skus" 表示在 Product 模型中也有一个名为 skus 的关系列表
    product: Mapped["Product"] = relationship(
        back_populates="skus",
        # "关联的商品对象（反向引用）"
    )
