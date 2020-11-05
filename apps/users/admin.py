from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from apps.users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass

# 添加表到后台管理系统中


admin.site.register(UserProfile, UserAdmin)
