# coding=utf-8
import xadmin
from users.models import ConfirmString, UserProfile


class ConfirmStringAdmin(object):
    list_display = ['user', 'code', 'create_time']
    search_fields = ['user']
    list_filter = ['user', 'code', 'create_time']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "后台"
    site_footer = "网站页脚.."
    # menu_style = "accordion"


xadmin.site.register(ConfirmString, ConfirmStringAdmin)
