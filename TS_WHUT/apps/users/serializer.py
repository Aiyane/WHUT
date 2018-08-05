from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

from .models import Folder
from operations.models import UserFolderImage, Follow
from images.models import ImageModel

User = get_user_model()


class ImageShowSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        # 图片链接
        return 'http://' + self.context['request']._request.META['HTTP_HOST'] + obj.image['avatar'].url

    class Meta:
        model = ImageModel
        fields = '__all__'


class CollectShipSerializer(serializers.ModelSerializer):
    image = ImageShowSerializer()

    class Meta:
        model = UserFolderImage
        fields = ('image', 'id')


class FolderOneSerializer(serializers.ModelSerializer):
    results = CollectShipSerializer(many=True)

    class Meta:
        model = Folder
        fields = ('name', 'id', 'nums', 'results', 'desc', 'add_time')


class FolderListSerializer(serializers.ModelSerializer):
    if_collect = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        data = []
        base_url = 'http://' + self.context['request']._request.META['HTTP_HOST']
        ships = UserFolderImage.objects.filter(folder_id=obj.id)
        for i, ship in enumerate(ships):
            if i == 4:
                return data
            data.append({
                "url": base_url + ship.image.image['avatar'].url
            })
        return data

    def get_if_collect(self, obj):
        image_id = self.context['request'].query_params.get('image-id')
        if image_id:
            ship = UserFolderImage.objects.filter(image_id=image_id, user=self.context['request'].user, folder=obj)
            if ship.count():
                return ship[0].id
        return False

    class Meta:
        model = Folder
        fields = ('name', 'id', 'nums', 'if_collect', 'image', 'desc', 'add_time')


class FolderCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if Folder.objects.filter(user=self.context['request'].user).count() > 50:
            raise serializers.ValidationError('收藏夹数量已达上限')
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = Folder
        fields = ('name', 'id', 'desc')


class FolderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('name', 'id', 'desc')


class UserListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    if_follow = serializers.SerializerMethodField()

    def get_if_follow(self, obj):
        ship = Follow.objects.filter(fan_id=self.context['request'].user.id, follow_id=obj.id)
        if ship:
            return ship[0].id
        return False

    def get_images(self, obj):
        data = []
        i = 0
        for image in ImageModel.objects.filter(user=obj)[::-1]:
            i += 1
            if i > 3:
                return data
            data.append({
                "url": 'http://' + self.context['request']._request.META['HTTP_HOST'] + image.image['avatar'].url,
                "id": image.id,
            })
        return data

    class Meta:
        model = User
        fields = ('id', 'if_sign', 'follow_nums', 'fan_nums', 'upload_nums', 'like_nums', 'desc',
                  'collection_nums', 'download_nums', 'image', 'username', 'images', 'if_follow')


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户名已经存在")])
    email = serializers.EmailField(required=True, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message="邮箱已经存在")])
    password = serializers.CharField(style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="用户名", help_text="用户名", required=False, allow_blank=True,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户名已经存在")])
    email = serializers.EmailField(required=False, allow_blank=True,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message="邮箱已经存在")])
    password = serializers.CharField(required=False, style={'input_type': 'password'}, help_text="密码",
                                     label="密码", write_only=True)

    def validate(self, attrs):
        if attrs.get("password"):
            attrs['password'] = make_password(attrs['password'])
        if attrs.get("email"):
            user = self.context['request'].user.if_active
            user.is_active = False
            user.save()
        return attrs

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'desc', 'username', 'image', 'gender', 'birthday')
