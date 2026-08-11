"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-10 11:06:06
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-10 11:13:57
FilePath: \\server-py\apps\\web-service\app\\core\\config.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from pydantic_settings import BaseSettings  # pyright: ignore[reportMissingImports]


class CommonSettings(BaseSettings):
    environment: str = "development"


class WebSettings(BaseSettings):
    app_name: str = "Awesome API"

    # 配置读取方式
    model_config = {
        "env_file": ".env",  # 文件夹的位置
        "env_prefix": "WEB_",  # 环境变量前缀
    }


# 实例化
common_settings = CommonSettings()
# 配置实例化
web_settings = WebSettings()

# 打印环境变量


def print_settings() -> None:
    """以表格形式打印当前生效的配置"""
    rows = [
        *common_settings.model_dump().items(),
        *((f"web.{key}", value) for key, value in web_settings.model_dump().items()),
    ]

    title = "App Settings"
    key_width = max(len(key) for key, _ in rows)
    value_width = max(len(str(value)) for _, value in rows)
    # "│ key : value │" 的内容宽度，并保证标题也能放得下
    inner_width = max(key_width + value_width + 5, len(title) + 2)

    print(f"┌{'─' * inner_width}┐")
    print(f"│ {title:<{inner_width - 2}} │")
    print(f"├{'─' * inner_width}┤")
    for key, value in rows:
        print(f"│ {key:<{key_width}} : {value!s:<{inner_width - key_width - 5}} │")
    print(f"└{'─' * inner_width}┘")


print_settings()
