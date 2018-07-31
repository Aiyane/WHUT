import django_filters

from .models import ImageModel


class ImageFilter(django_filters.rest_framework.FilterSet):
    """
    图片的过滤类
    """
    class Meta:
        model = ImageModel
        fields = ['pattern', 'user']
