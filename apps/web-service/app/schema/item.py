"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-11 16:50:30
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-11 19:55:46
FilePath: \server-py\apps\web-service\app\schema\item.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from pydantic import BaseModel, Field


class Item(BaseModel):
    item_id: int | None = Field(
        # 1. default=None：设置字段的默认值为 None
        #    意味着创建对象时，如果不传 item_id，这个字段就是 None
        #    由于类型是 int | None，这允许该字段在数据中完全缺失
        default=None,
        # 2. title="商品ID"：给字段起一个人类可读的显示名称
        #    主要用于自动生成 API 文档（如 Swagger/OpenAPI）
        #    在文档界面中，这个字段会显示为 "商品ID"
        title="商品ID",
        # 3. description="..."：对字段的详细解释说明
        #    告诉 API 调用者这个字段的业务含义和使用规则
        #    同样会显示在自动生成的接口文档中
        description="商品的唯一标识符，在创建商品时可忽略，系统会自动生成。",
        # 4. ge=1：数值校验约束（Greater than or Equal to）
        #    限定传入的数值必须 >= 1
        #    如果传入了 0 或 -5，Pydantic 会抛出验证错误
        #    注意：因为 default=None，None 不会触发此校验，只有传入具体整数时才校验
        ge=1,
        # 5. examples=[1, 2, 3]：给字段提供示例值
        #    用于文档展示，告诉调用者典型合法数据长什么样
        #    Swagger 界面上会显示 "示例: 1, 2, 3"
        examples=[1, 2, 3],
    )
    name: str = Field(
        ...,
        title="商品名称",
        description="商品的显示名称，长度必须在2到10个字符之间。",
        min_length=2,
        max_length=10,
        examples=["无线鼠标"],
    )

    price: float = Field(
        default=0.0,
        title="商品价格",
        description="商品的销售价格，必须大于或等于0。",
        ge=0.0,
        examples=[19.99, 0.0, 100.5],
    )
