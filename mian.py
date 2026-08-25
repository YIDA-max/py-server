# main.py
from Depends import Depends


def check_permission(user: str) -> bool:
    print(f"验证用户{user}权限")
    return True


def ali_oss_upload(user: str, file: str, has_permission=Depends(check_permission)):
    if not has_permission(user):
        raise Exception("权限不足")
    print(f"阿里云，{file} 上传中...")


def upload_file(user: str, file: str, oss_upload=Depends(ali_oss_upload)):
    print("上传准备")
    oss_upload(user, file)  # 注意这里传入的是函数本身
    print("上传成功")


# 正常情况
upload_file("张三", "1.txt")


# 特殊情况：希望切换为腾讯云怎么办？？？
def tencent_oss_upload(user: str, file: str, has_permission=Depends(check_permission)):
    if not has_permission(user):
        raise Exception("权限不足")
    print(f"腾讯云，{file} 上传中...")


Depends.override(ali_oss_upload, tencent_oss_upload)
upload_file("张三", "2.txt")


# 测试环境：希望使用假的oss上传怎么办？？？
def fake_upload(user: str, file: str, has_permission=Depends(check_permission)):
    if not has_permission(user):
        raise Exception("权限不足")
    print(f"模拟，{file} 上传中...")


def fake_check_permission(user: str) -> bool:
    print(f"模拟：验证用户{user}权限")
    return True


Depends.clear_override()
Depends.override(ali_oss_upload, fake_upload)
Depends.override(check_permission, fake_check_permission)
upload_file("张三", "3.txt")
