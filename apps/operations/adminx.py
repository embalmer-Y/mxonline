import xadmin

from apps.operations.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse
from apps.operations.models import Banner



class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ["user", "course", "comments", 'add_time']
    search_fields = ["user", "course", "comments"]
    list_filter = ["user", "course", 'add_time']


class UserFavoriteAdmin(object):
    list_display = ["user", "fav_id", "fav_type", 'add_time']  # 列表页所需要显示的字段
    search_fields = ["user", "fav_id", "fav_type"]  # 搜索框字段
    list_filter = ["user", "fav_id", "fav_type", 'add_time']  # 过滤器设置


class UserMessageAdmin(object):
    list_display = ["user", "message", "has_read", 'add_time']  # 列表页所需要显示的字段
    search_fields = ["user", "message", "has_read"]  # 搜索框字段
    list_filter = ["user", "message", "has_read", 'add_time']  # 过滤器设置


class UserCourseAdmin(object):
    list_display = ["user", "course", 'add_time']  # 列表页所需要显示的字段
    search_fields = ["user", "course"]  # 搜索框字段
    list_filter = ["user", "course", 'add_time']  # 过滤器设置


class BannerAdmin(object):
    list_display = ["title", "image", 'url', 'index']  # 列表页所需要显示的字段
    search_fields = ["title", "image", 'url', 'index']   # 搜索框字段
    list_filter = ["title", "image", 'url', 'index']   # 过滤器设置


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)