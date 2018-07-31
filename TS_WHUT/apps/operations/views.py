from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic.base import View
from django.contrib.auth import get_user_model
from django.shortcuts import render

from .serializer import (LikeSerializer, DownloadSerializer, FollowSerializer, CollectSerializer,
                         LikeListSerializer, DownloadListSerializer, FollowListSerializer, FanListSerializer)
from .models import LikeShip, Follow, UserFolderImage, DownloadShip
from users.models import EmailVerifyRecord, UserMessage
from utils.send_email import send_register_email

User = get_user_model()


class FollowUserViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取全部关注用户
    """
    serializer_class = FollowListSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(fan=self.request.user)


class FanUserViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取全部粉丝
    """
    serializer_class = FanListSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(follow=self.request.user)


class CollectViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
        添加图片到收藏夹
    destroy:
        从收藏夹删除图片
    """
    serializer_class = CollectSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 删除只能是该用户收藏
        return UserFolderImage.objects.filter(user=self.request.user)


class LikeViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户点赞图片
    create:
        点赞一张图片
    destroy:
        取消点赞一张图片
    """
    serializer_class = LikeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return LikeListSerializer
        return LikeSerializer

    def get_queryset(self):
        # 删除只能是点赞者
        return LikeShip.objects.filter(user=self.request.user)


class FollowViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
        关注用户
    destroy:
        取消关注
    """
    serializer_class = FollowSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return FollowSerializer

    def get_queryset(self):
        # 取消只能是关注者
        return Follow.objects.filter(fan=self.request.user)


class DownloadViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    create:
        下载图片
    list:
        获取用户下载图片
    """
    serializer_class = DownloadSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DownloadShip.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return DownloadListSerializer
        return DownloadSerializer

    def create(self, request, *args, **kwargs):
        # 下载图片返回原图url
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ship = self.perform_create(serializer)

        re_dict = serializer.data
        re_dict['url'] = 'http://' + self.request._request.META['HTTP_HOST'] + ship.image.image.url

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class ActiveUserView(View):
    """
    用户激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.send_email
                # 得到一个用户信息邮箱与传来的邮箱验证邮箱相同的用户信息实例
                user = User.objects.get(email=email)
                user.if_active = True
                user.save()
            # 验证成功, 返回主页
            return render(request, 'index.html')


class ResetView(View):
    def post(self, request):
        """
        忘记密码
        """
        email = request.POST.get("email", "")
        if not email:
            response = Response({"non_field_errors": ["参数错误"]})
            response.status_code = 400
            return response
        user = User.objects.filter(email=email)[0]
        if user and user.email == email:
            # 保存用户信息
            user_message = UserMessage()
            user_message.user = user
            user_message.message = "图说理工网修改密码"
            user_message.save()

            send_register_email(email, "forget")  # 发送验证邮箱
            return Response(status.HTTP_201_CREATED)
        else:
            response = Response({"non_field_errors": ["没有该用户"]})
            response.status_code = 404
            return response


class ResetPwdView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)  # 这里的all_records是多个邮箱验证实例，因为验证码可能相同
        if all_records:
            for record in all_records:
                email = record.send_email
                user = User.objects.get(email=email)  # 得到一个用户信息邮箱与传来的邮箱验证邮箱相同的用户信息实例
                return render(request, "password_reset.html", {"user": user})
        else:
            return render(request, "active_fail.html")


class ChangePasswordView(View):
    def post(self, request):
        password = request.POST.get("password")
        username = request.POST.get("username")
        users = User.objects.filter(username=username)
        if users:
            user = users[0]
            user.password = password
            user.save()
            # 修改成功提示去登录
            pass
        else:
            # 失败
            pass