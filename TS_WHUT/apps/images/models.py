from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from easy_thumbnails.fields import ThumbnailerImageField

from utils.storage import ImageStorage

User = get_user_model()


class BannerModel(models.Model):
    # 轮播图
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", storage=ImageStorage(), verbose_name="轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name="访问地址")
    if_show = models.BooleanField(default=False, verbose_name="是否显示")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ImageModel(models.Model):
    # 图片
    image = ThumbnailerImageField(upload_to="images/%Y/%m", storage=ImageStorage(),
                                  verbose_name="图片", max_length=100, null=True, blank=True)
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    if_active = models.BooleanField(default=False, verbose_name="是否通过审核")
    desc = models.CharField(max_length=200, verbose_name="描述", null=True, blank=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True, verbose_name="上传人")
    pattern = models.CharField(max_length=10, verbose_name="格式", default="png")
    like_nums = models.IntegerField(default=0, verbose_name="点赞数")
    cates = models.CharField(max_length=200, verbose_name="种类字符串", default="")
    collection_nums = models.IntegerField(default=0, verbose_name="收藏数")
    download_nums = models.IntegerField(default=0, verbose_name="下载量")
    name = models.CharField(max_length=20, verbose_name="名字", default="")

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GroupImage(models.Model):
    # 图片种类
    name = models.CharField(verbose_name="图片分类", max_length=20)
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    image = models.ForeignKey(ImageModel, models.CASCADE, verbose_name="图片")

    class Meta:
        verbose_name = "图片种类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    # 图片评论
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, verbose_name="图片")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="用户", related_name="speaker")
    reply = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="回复人", related_name="listen")
    content = models.CharField(max_length=200, verbose_name="评论")
    like = models.IntegerField(default=0, verbose_name="点赞数")

    class Meta:
        verbose_name = "图片评论"
        verbose_name_plural = verbose_name
