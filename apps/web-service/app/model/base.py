# model/base.py
from datetime import datetime

from sqlalchemy import DateTime, Identity, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """
    SQLAlchemy ORM 的基类。
    所有数据模型类（如 Product、Category）都需要继承这个类。
    它提供了与数据库交互的基础能力（表映射、会话管理、查询构造等）。
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        自动生成数据库表名。
        规则：将类名转换为小写，作为表名。

        例如：
            class Product(Base) → 表名为 "product"
            class Category(Base) → 表名为 "category"

        declared_attr.directive 表示这是一个类级别的属性生成器，
        在类定义时会被调用，将返回值设为 __tablename__。

        好处：无需在每个子类中手动写 __tablename__，统一且不易出错。
        """
        return cls.__name__.lower()


class IDMixin:
    """
    主键混入类（Mixin）。
    为继承它的模型自动添加一个自增主键字段 id。

    混入类（Mixin）是一种代码复用机制：
    通过多继承，将通用字段或方法组合到多个模型类中。
    """

    # id 字段：整数类型，使用数据库自增（Identity）
    # Identity() 是 SQLAlchemy 2.0 推荐的自增写法（替代旧的 autoincrement=True）
    # primary_key=True 指定该字段为主键
    id: Mapped[int] = mapped_column(Identity(), primary_key=True)


class TimestampMixin:
    """
    时间戳混入类（Mixin）。
    为继承它的模型自动添加两个时间字段：
        - created_at：创建时间（插入时自动设为当前时间）
        - updated_at：更新时间（插入时设为当前时间，更新时自动刷新）

    适用于几乎所有需要记录时间审计信息的业务表。
    """

    # created_at：创建时间，类型为 datetime
    # DateTime：对应数据库的 DATETIME 或 TIMESTAMP 类型（取决于数据库）
    # server_default=func.now()：数据库级别的默认值，使用数据库当前时间
    #   注意：func.now() 在 SQLAlchemy 中表示数据库的 now()/CURRENT_TIMESTAMP 函数
    #   这样设置后，插入记录时，即使 Python 端不传值，数据库也会自动填入当前时间
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # updated_at：更新时间
    # 同样使用 DateTime 类型，server_default=func.now() 插入时默认当前时间
    # onupdate=func.now()：更新记录时，该字段自动更新为当前时间
    #   这是 SQLAlchemy 层面的特性，ORM 会在执行 update 时自动设置
    # 注意：如果通过纯 SQL 更新（不经过 ORM），该字段不会自动更新，需自行处理
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
