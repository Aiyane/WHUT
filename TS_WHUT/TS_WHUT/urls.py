"""TS_WHUT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
import xadmin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
# from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from images.views import ImageViewset, BannerViewset
from operations.views import (LikeViewset, DownloadViewset, FollowViewset, ActiveUserView,
                              CollectViewset, FollowUserViewset, FanUserViewset)
from users.views import FolderViewset, UserViewset, Login

router = DefaultRouter()
# 图片API
router.register('images', ImageViewset, base_name="images")
# 轮播图API
router.register('banners', BannerViewset, base_name="banners")
# 收藏夹API
router.register('folders', FolderViewset, base_name="folders")
# 用户API
router.register('users', UserViewset, base_name="users")
# 关注者API
router.register('followers', FollowUserViewset, base_name="followings")
# 粉丝API
router.register('fans', FanUserViewset, base_name="fans")
# 点赞API
router.register('like', LikeViewset, base_name="like")
# 下载API
router.register('download', DownloadViewset, base_name="download")
# 关注API
router.register('follow', FollowViewset, base_name="follow")
# 收藏API
router.register('collect', CollectViewset, base_name="collect")


urlpatterns = [
    # xadmin
    path('admin/', xadmin.site.urls),
    # rest框架用户认证
    path('api-auth/', include('rest_framework.urls')),
    # 文档
    path('docs/', include_docs_urls(title="图说理工")),
    # drf 自带token认证模式
    path('api-token-auth/', views.obtain_auth_token),
    # jwt认证接口, 登录
    path('login/', Login.as_view()),
    # 全部API
    path('', include(router.urls)),
    # 注册验证
    path('active/<str:active_code>/', ActiveUserView.as_view(), name="user_active"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)