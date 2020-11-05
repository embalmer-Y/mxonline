from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    # 修改后台管理系统显示的名称
    verbose_name = "用户"
