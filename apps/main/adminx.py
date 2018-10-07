# coding=utf-8
import xadmin
from main.models import CourseGroup, CourseItem, AppVersion
from users.models import ConfirmString, UserProfile


class CourseGroupAdmin(object):
    list_display = ['name', 'school_class', 'share', 'user', 'create_time']
    search_fields = ['name', 'school_class']
    list_filter = ['create_time', 'share']


class CourseItemAdmin(object):
    list_display = ['name', 'teacher', 'location', 'color', 'time_which_day',
                    'start_node', 'node_count', 'create_time']
    search_fields = ['name']
    list_filter = ['group_id']


class AppVersionAdmin(object):
    list_display = ['version_code', 'version_name', 'describe', 'release', 'create_time']
    search_fields = ['version_code']
    list_filter = ['release']


xadmin.site.register(CourseGroup, CourseGroupAdmin)
xadmin.site.register(CourseItem, CourseItemAdmin)
xadmin.site.register(AppVersion, AppVersionAdmin)
