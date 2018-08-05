from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend

from .serializer import (FolderCreateSerializer, FolderListSerializer, FolderOneSerializer, FolderUpdateSerializer,
                         UserListSerializer, UserCreateSerializer, UserUpdateSerializer)
from .models import Folder, UserMessage
from utils.send_email import send_register_email
from .filters import UsersFilter

User = get_user_model()


# class Login(ObtainJSONWebToken):
#     """
#     重载ObtainJSONWebToken的post方法, 使得未激活用户无法登录
#     """
#     def post(self, request, *args, **kwargs):
#         jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             user = serializer.object.get('user') or request.user
#             if not user.if_active:
#                 return Response({"non_field_errors": ["用户未激活"]}, status=status.HTTP_400_BAD_REQUEST)
#
#             token = serializer.object.get('token')
#             response_data = jwt_response_payload_handler(token, user, request)
#             response = Response(response_data)
#             if api_settings.JWT_AUTH_COOKIE:
#                 expiration = (datetime.utcnow() +
#                               api_settings.JWT_EXPIRATION_DELTA)
#                 response.set_cookie(api_settings.JWT_AUTH_COOKIE,
#                                     token,
#                                     expires=expiration,
#                                     httponly=True)
#             return response
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FolderViewset(viewsets.ModelViewSet):
    """
    list:
        获取用户全部收藏夹
    create:
        创建一个收藏夹
    retrieve:
        获取一个收藏夹的全部图片
    update:
        修改收藏夹名字
    destroy:
        删除一个收藏夹
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 只能对自己的收藏夹操作
        return Folder.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return FolderCreateSerializer
        elif self.action == 'list':
            return FolderListSerializer
        elif self.action == 'retrieve':
            return FolderOneSerializer
        return FolderUpdateSerializer


class UserPagination(PageNumberPagination):
    """
    图片分页
    page_size: 每页大小
    page_size_query_param: 每页大小参数名
    page_query_param: 第几页参数名
    max_page_size: 最大页数
    """
    page_size = 8
    page_size_query_param = 'num'
    page_query_param = "page"
    max_page_size = 100


class UserViewset(viewsets.ModelViewSet):
    """
    list:
        获取全部用户, (按下载量,收藏量,关注量排序)
    create:
        注册用户
    retrieve:
        获取用户信息
    update:
        修改用户信息
    destroy:
        删除用户
    """
    serializer_class = UserListSerializer
    queryset = User.objects.filter(is_active=True)
    pagination_class = UserPagination
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_class = UsersFilter
    ordering_fields = ('fan_nums', 'download_nums', 'collection_nums')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        if self.action == 'destroy':
            return User.objects.filter(id=self.request.user.id)
        elif self.action == 'update':
            return User.objects.filter(id=self.request.user.id)
        return User.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action == "create":
            return []
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        return UserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        pwd = make_password(user.password)
        user.password = pwd
        user.is_active = False
        user.save()
        headers = self.get_success_headers(serializer.data)

        # 写入欢迎注册消息
        user_message = UserMessage()
        user_message.user = user
        user_message.message = "欢迎注册图说理工网"
        user_message.save()

        # 发送验证邮箱
        send_register_email(user.email, "register")

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = self.perform_update(serializer)

        if not user.is_active:
            user_message = UserMessage()
            user_message.user = user
            user_message.message = "图说理工网-验证个人信息修改"
            user_message.save()
            # 发送验证邮箱
            send_register_email(user.email, "register")

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        return serializer.save()
