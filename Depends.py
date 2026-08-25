"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-25 16:57:03
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-25 17:02:08
FilePath: \server-py\Depends.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Depends:
    """
    一个轻量级的依赖注入（DI）辅助类，用于实现“控制反转（IoC）”思想。

    该类包装一个可调用对象（函数或类），并允许在运行时通过全局覆盖机制替换其实现，
    从而方便在测试或不同环境下更换依赖，而无需修改调用方代码。

    典型用法：
        1. 在业务代码中，使用 `Depends(some_function)` 作为依赖的占位符。
        2. 在测试或配置阶段，调用 `Depends.override(original, replacement)`
           将 `original` 替换为 `replacement`。
        3. 调用被包装的对象时，实际执行的是当前生效的实现。

    注意：这是一个全局单例级别的覆盖，适用于中小型项目或测试场景。
    """

    # 类变量：存储所有被覆盖的可调用对象映射
    # key: 原始可调用对象, value: 替换用的可调用对象
    _overrides: dict[Callable[..., Any], Callable[..., Any]] = {}

    def __init__(self, func: Callable[..., Any]) -> None:
        """
        初始化 Depends 实例。

        :param func: 被包装的原始可调用对象（函数、类或方法）。
        """
        self.func = func

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        使得 Depends 实例可以像函数一样被调用。

        实际调用时，会检查 `_overrides` 中是否存在当前 `func` 的替换，
        如果存在则调用替换函数，否则调用原始函数。

        :param args: 位置参数
        :param kwds: 关键字参数
        :return: 被调用函数的返回值
        """
        # 获取实际应该执行的可调用对象（若被覆盖则使用覆盖版本）
        actual = self._overrides.get(self.func, self.func)
        return actual(*args, **kwds)

    @classmethod
    def override(
        cls,
        original: Callable[..., Any],
        replacement: Callable[..., Any],
    ) -> None:
        """
        全局覆盖一个原始可调用对象，将其替换为另一个实现。

        此方法通常用于测试环境中的 Mock，或在不同运行环境下切换实现。

        :param original: 需要被覆盖的原始可调用对象（通常与 Depends 包装的对象相同）
        :param replacement: 替换后的新可调用对象
        """
        cls._overrides[original] = replacement

    @classmethod
    def clear_override(cls, func: Callable[..., Any] | None = None) -> None:
        """
        清除全局覆盖映射中的指定条目或全部清空。

        :param func: 可选，指定要清除覆盖的原始可调用对象。
                     如果为 None，则清空所有覆盖。
        """
        if func is not None:
            cls._overrides.pop(func, None)  # 移除指定键，不存在时忽略
        else:
            cls._overrides.clear()  # 清空整个覆盖字典
