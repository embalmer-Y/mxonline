from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operations.models import UserFavorite, UserCourse, CourseComments


class VideoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.chick_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        # 查询用户是否关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__chick_nums")[:5]
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        course_resource = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resource": course_resource,
            "related_courses": related_courses,
            "video": video,
        })

class CourseCommentView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.chick_nums += 1
        course.save()
        # 查询用户是否关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        comments = CourseComments.objects.filter(course=course)

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__chick_nums")[:5]
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        course_resource = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "course_resource": course_resource,
            "related_courses": related_courses,
            "comments": comments
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.chick_nums += 1
        course.save()

        # 查询用户是否关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__chick_nums")[:5]
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        course_resource = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resource": course_resource,
            "related_courses": related_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程详情
        """
        course = Course.objects.get(id=int(course_id))
        course.chick_nums += 1
        course.save()

        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 通过课程的tag做推荐
        # tag = course.tag
        # related_courses = list()
        # if tag:
        #     related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course.id])[:3]
        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """
        获取课程列表信息
        """
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-chick_nums")[:3]

        # 搜索关键词
        keywords = request.GET.get('keywords', '')
        s_type = 'course'
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) |
                                             Q(detail__icontains=keywords))

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by('-chick_nums')

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=5, request=request)

        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            'keywords': keywords,
            's_type': s_type
        })
