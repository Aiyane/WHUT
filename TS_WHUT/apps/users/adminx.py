import xadmin
from xadmin import views

from .models import UserProfile, EmailVerifyRecord, Folder, UserMessage


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    site_title = "图说理工后台管理系统"
    site_footer = "图说理工在线网"
    menu_style = 'Readable'


class UserProfileAdmin(object):
    list_display = ['username', 'email', 'is_staff', 'mobile', 'number', 'gender', 'birthday']
    search_fields = ['number', 'email', 'username', 'mobile']
    list_filter = ['is_staff']


class EmailVerifyRecordAdmin(object):
    list_display = ['send_type', 'code', 'send_email', 'send_time']
    search_fields = ['send_email', 'code']
    list_filter = ['send_time', 'send_type']


class FolderAdmin(object):
    list_display = ['name', 'user', 'nums', 'add_time']
    search_fields = ['name', 'user', 'nums']
    list_filter = ['user', 'add_time']


class UserMessageAdmin(object):
    list_display = ['message', 'user', 'post_user', 'has_read', 'add_time']
    search_fields = ['message', 'user', 'post_user', 'has_read']
    list_filter = ['user', 'post_user', 'has_read', 'add_time']


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Folder, FolderAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
