from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ImageModel, BannerModel, Comment
from .serializer import ImageSerializer, ImageCreateSerializer, BannerSerializer, CommentListSerializer, CommentCreateSerializer
from .filters import ImageFilter, CommentFilter


class ImagePagination(PageNumberPagination):
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


class ImageViewset(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    list:
        显示所有图片,时间倒序
    create:
        上传一张图片
    retrieve:
        显示一张图片
    destroy:
        删除一张图片
    """
    serializer_class = ImageSerializer
    pagination_class = ImagePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = ImageFilter
    search_fields = ('cates', 'name', 'desc')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # 删除只能是上传者
        if self.action == 'destroy':
            return ImageModel.objects.filter(user=self.request.user)
        return ImageModel.objects.filter(if_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ImageSerializer
        elif self.action == 'create':
            return ImageCreateSerializer
        return ImageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset[::-1])
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BannerModel.objects.filter(if_show=True)
    serializer_class = BannerSerializer


class CommentViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        列出单张图片的全部评论
    create:
        添加评论
    """
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CommentFilter
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        return CommentCreateSerializer
