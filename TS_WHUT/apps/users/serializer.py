from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from .models import Folder
from operations.models import UserFolderImage
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
    images = CollectShipSerializer(many=True)

    class Meta:
        model = Folder
        fields = ('name', 'id', 'nums', 'images')


class FolderListSerializer(serializers.ModelSerializer):
    if_collect = serializers.SerializerMethodField()

    def get_if_collect(self, obj):
        image_id = self.context['request'].query_params.get('image-id')
        if image_id:
            if UserFolderImage.objects.filter(image_id=image_id, user=self.context['request'].user, folder=obj).count():
                return True
        return False

    class Meta:
        model = Folder
        fields = ('name', 'id', 'nums', 'if_collect')


class FolderCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = Folder
        fields = ('name', 'id')


class FolderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('name', 'id')


class UserListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

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

    class Meta:
        model = User
        fields = ('id', 'if_sign', 'follow_nums', 'fan_nums', 'upload_nums', 'like_nums',
                  'collection_nums', 'download_nums', 'image', 'username', 'images')


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
    username = serializers.CharField(label="用户名", help_text="用户名", required=False, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户名已经存在")])
    email = serializers.EmailField(required=False, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message="邮箱已经存在")])
    password = serializers.CharField(required=False, style={'input_type': 'password'}, help_text="密码",
                                     label="密码", write_only=True)

    def validate(self, attrs):
        if attrs['email']:
            user = self.context['request'].user.if_active
            user.if_active = False
            user.save()
        return attrs

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'image', 'gender', 'birthday', 'if_sign')
