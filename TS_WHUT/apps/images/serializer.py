from rest_framework import serializers
from .models import ImageModel, BannerModel
from django.contrib.auth import get_user_model
from operations.models import LikeShip, UserFolderImage, Follow

User = get_user_model()


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerModel
        fields = ('image', 'url', 'title')


class UserBrifSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('image', 'id', 'username')


class ImageSerializer(serializers.ModelSerializer):
    user = UserBrifSerializer()
    image = serializers.SerializerMethodField()
    if_like = serializers.SerializerMethodField()
    if_collect = serializers.SerializerMethodField()
    if_follow = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()

    def get_image(self, obj):
        # 图片链接
        return 'http://' + self.context['request']._request.META['HTTP_HOST'] + obj.image['avatar'].url

    def get_if_like(self, obj):
        # 是否点赞图片
        if LikeShip.objects.filter(user=self.context['request'].user, image_id=obj.id).count():
            return True
        return False

    def get_if_collect(self, obj):
        # 是否收藏图片
        if UserFolderImage.objects.filter(user=self.context['request'].user, image_id=obj.id).count():
            return True
        return False

    def get_if_follow(self, obj):
        # 是否关注上传者
        if Follow.objects.filter(fan=self.context['request'].user, follow=obj.user).count():
            return True
        return False

    def get_height(self, obj):
        # 图片高
        return obj.image.height

    def get_width(self, obj):
        # 图片宽
        return obj.image.width

    class Meta:
        model = ImageModel
        fields = '__all__'


class ImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    cates = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = ImageModel
        fields = ('desc', 'cates', 'name', 'image')
