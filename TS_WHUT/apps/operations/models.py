from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

from images.models import Comment, ImageModel
from users.models import Folder

User = get_user_model()


class Follow(models.Model):
    # 关注用户
    follow = models.ForeignKey(User, related_name="follow_user", on_delete=models.CASCADE, verbose_name="被关注者")
    fan = models.ForeignKey(User, related_name="fan_user", on_delete=models.CASCADE, verbose_name="粉丝")
    add_time = models.DateField(default=datetime.now, verbose_name="关注时间")

    class Meta:
        verbose_name = "关注用户"
        verbose_name_plural = verbose_name


class LikeShip(models.Model):
    # 点赞图片
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="用户名")
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, verbose_name="图片")
    add_time = models.DateField(default=datetime.now, verbose_name="点赞时间")

    class Meta:
        verbose_name = "点赞图片"
        verbose_name_plural = verbose_name


class DownloadShip(models.Model):
    # 下载图片
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="用户名")
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, verbose_name="图片")
    add_time = models.DateField(default=datetime.now, verbose_name="下载时间")

    class Meta:
        verbose_name = "下载图片"
        verbose_name_plural = verbose_name


class CommentLike(models.Model):
    # 点赞评论
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="评论")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="用户")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "点赞评论"
        verbose_name_plural = verbose_name


class UserFolderImage(models.Model):
    # 收藏图片
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, verbose_name="收藏夹", related_name="results")
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, verbose_name="图片")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "收藏图片"
        verbose_name_plural = verbose_name


class Application(models.Model):
    # 申请签约
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="申请人")
    status = models.CharField(max_length=11, default="contract", verbose_name="申请签约状态",
                              choices=(("1", "用户同意合同"),
                                       ("2", "等待审核"),
                                       ("4", "未通过审核"),
                                       ("3", "已完成")))
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    url = models.CharField(null=True, blank=True, verbose_name="作品集链接", max_length=100)

    class Meta:
        verbose_name = "申请签约"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
