import xadmin

from apps.organizations.models import Teacher, CourseOrg, City


class CourseOrgAdmin(object):
    list_display = ["name", "desc", "click_nums", "fav_nums"]  # 列表页所需要显示的字段
    search_fields = ["name", "desc", "click_nums", "fav_nums"]  # 搜索框字段
    list_filter = ["name", "desc", "click_nums", "fav_nums"]  # 过滤器设置


class TeacherAdmin(object):
    list_display = ["org", "name", "work_years", "work_company", "click_nums", "fav_nums"]  # 列表页所需要显示的字段
    search_fields = ["org", "name", "work_years", "work_company"]  # 搜索框字段
    list_filter = ["org", "name", "work_years", "work_company"]  # 过滤器设置


class CityAdmin(object):
    list_display = ["id", "name", "desc"]  # 列表页所需要显示的字段
    search_fields = ["name", "desc"]  # 搜索框字段
    list_filter = ["name", "desc", "add_time"]  # 过滤器设置
    list_editable = ["name", "desc"]  # 编辑功能


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
