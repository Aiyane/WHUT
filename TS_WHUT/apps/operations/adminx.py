import xadmin

from .models import Follow, LikeShip, DownloadShip, CommentLike, UserFolderImage


class FollowAdmin(object):
    list_display = ['follow', 'fan', 'add_time']
    search_fields = ['follow', 'fan']
    list_filter = ['follow', 'fan', 'add_time']


class LikeShipAdmin(object):
    list_display = ['user', 'image', 'add_time']
    search_fields = ['user', 'image']
    list_filter = ['user', 'image', 'add_time']


class DownloadShipAdmin(object):
    list_display = ['user', 'image', 'add_time']
    search_fields = ['user', 'image']
    list_filter = ['user', 'image', 'add_time']


class CommentLikeAdmin(object):
    list_display = ['comment', 'user', 'add_time']
    search_fields = ['comment', 'user']
    list_filter = ['comment', 'user', 'add_time']


class UserFolderImageAdmin(object):
    list_display = ['folder', 'user', 'image', 'add_time']
    search_fields = ['folder', 'user', 'image']
    list_filter = ['folder', 'user', 'image', 'add_time']

xadmin.site.register(Follow, FollowAdmin)
xadmin.site.register(LikeShip, LikeShipAdmin)
xadmin.site.register(DownloadShip, DownloadShipAdmin)
xadmin.site.register(CommentLike, CommentLikeAdmin)
xadmin.site.register(UserFolderImage, UserFolderImageAdmin)