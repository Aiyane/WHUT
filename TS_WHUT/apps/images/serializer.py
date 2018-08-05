from rest_framework import serializers
from .models import ImageModel, BannerModel, Comment
from django.contrib.auth import get_user_model
from operations.models import LikeShip, UserFolderImage, Follow, CommentLike

User = get_user_model()


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerModel
        fields = ('image', 'url', 'title')


class UserBrifSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('image', 'id', 'username', 'upload_nums', 'fan_nums')


class ImageSerializer(serializers.ModelSerializer):
    user = UserBrifSerializer()
    image = serializers.SerializerMethodField()
    if_like = serializers.SerializerMethodField()
    if_collect = serializers.SerializerMethodField()
    if_follow = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        # 图片大小
        return obj.image.size

    def get_image(self, obj):
        # 图片链接
        return 'http://' + self.context['request']._request.META['HTTP_HOST'] + obj.image['avatar'].url

    def get_if_like(self, obj):
        # 是否点赞图片
        ship = LikeShip.objects.filter(user_id=self.context['request'].user.id, image_id=obj.id)
        if ship.count():
            return ship[0].id
        return False

    def get_if_collect(self, obj):
        # 是否收藏图片
        ship = UserFolderImage.objects.filter(user_id=self.context['request'].user.id, image_id=obj.id)
        if ship.count():
            return ship[0].id
        return False

    def get_if_follow(self, obj):
        # 是否关注上传者
        ship = Follow.objects.filter(fan_id=self.context['request'].user.id, follow_id=obj.user.id)
        if ship.count():
            return ship[0].id
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


class CommentListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    if_like = serializers.SerializerMethodField()

    def get_if_like(self, obj):
        # 是否点赞
        user = self.context['request'].user
        ship = CommentLike.objects.filter(user_id=user.id, comment_id=obj.id)
        if ship.count():
            return ship[0].id
        return False

    def get_image(self, obj):
        # 验证参数
        image = self.context['request'].query_params.get('image')
        if image:
            return int(image)
        raise serializers.ValidationError('参数错误!')

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('image', 'user', 'reply', 'content')
