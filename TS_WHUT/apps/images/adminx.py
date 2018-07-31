import xadmin

from .models import BannerModel, ImageModel, GroupImage, Comment


class BannerModelAdmin(object):
    list_display = ['title', 'url', 'if_show', 'add_time']
    search_fields = ['title', 'url', 'if_show']
    list_filter = ['title', 'if_show', 'add_time']


class ImageModelAdmin(object):
    list_display = ['name', 'user', 'if_active', 'desc', 'pattern', 'cates', 'add_time']
    search_fields = ['user', 'name', 'desc', 'pattern']
    list_filter = ['user', 'name', 'if_active', 'desc', 'pattern', 'cates', 'add_time']


class GroupImageAdmin(object):
    list_display = ['name', 'image', 'add_time']
    search_fields = ['name', 'image']
    list_filter = ['name', 'image', 'add_time']


class CommentAdmin(object):
    list_display = ['content', 'like', 'image', 'user', 'reply', 'add_time']
    search_fields = ['content', 'like', 'image', 'user', 'reply']
    list_filter = ['content', 'like', 'image', 'user', 'reply', 'add_time']

xadmin.site.register(BannerModel, BannerModelAdmin)
xadmin.site.register(ImageModel, ImageModelAdmin)
xadmin.site.register(GroupImage, GroupImageAdmin)
xadmin.site.register(Comment, CommentAdmin)
