from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import LikeShip, DownloadShip, Follow, UserFolderImage


@receiver(post_save, sender=UserFolderImage)
def create_collect_num(sender, instance=None, created=False, **kwargs):
    """
    当收藏图片动作发生
    """
    if created:
        # 图片收藏数加1
        image = instance.image
        image.collection_nums += 1
        image.save()
        # 图片上传者总收藏数加1
        user = image.user
        user.collection_nums += 1
        user.save()
        # 收藏夹图片数量加1
        folder = instance.folder
        folder.nums += 1
        folder.save()


@receiver(pre_delete, sender=UserFolderImage)
def delete_collect_num(sender, instance=None, **kwargs):
    """
    当取消收藏图片动作发生 
    """
    # 图片收藏数减1
    image = instance.image
    image.collection_nums -= 1
    image.save()
    # 图片上传者总收藏数减1
    user = image.user
    user.collection_nums -= 1
    user.save()
    # 收藏夹图片数量减1
    folder = instance.folder
    folder.nums -= 1
    folder.save()


@receiver(post_save, sender=Follow)
def create_follow_num(sender, instance=None, created=False, **kwargs):
    """
    当关注动作发生 
    """
    if created:
        # 粉丝的关注者数量加1
        fan = instance.fan
        fan.follow_nums += 1
        fan.save()
        # 被关注着的粉丝数量加1
        follow = instance.follow
        follow.fan_nums += 1
        follow.save()


@receiver(pre_delete, sender=Follow)
def delete_follow_num(sender, instance=None, **kwargs):
    """
    当取消关注动作发生
    """
    # 粉丝的关注者数量减1
    fan = instance.fan
    fan.follow_nums -= 1
    fan.save()
    # 被关注着的粉丝数量减1
    follow = instance.follow
    follow.fan_nums -= 1
    follow.save()


@receiver(post_save, sender=LikeShip)
def create_like_num(sender, instance=None, created=False, **kwargs):
    """
    当点赞图片动作发生
    """
    if created:
        # 图片点赞量加1
        image = instance.image
        image.like_nums += 1
        image.save()
        # 用户总图片点赞量加1
        user = image.user
        user.like_nums += 1
        user.save()


@receiver(pre_delete, sender=LikeShip)
def delete_like_num(sender, instance=None, **kwargs):
    """
    当取消点赞图片动作发生 
    """
    # 图片点赞量减1
    image = instance.image
    image.like_nums -= 1
    image.save()
    # 用户总图片点赞量减1
    user = image.user
    user.like_nums -= 1
    user.save()


@receiver(post_save, sender=DownloadShip)
def create_download_num(sender, instance=None, created=False, **kwargs):
    """
    当关注点赞图片动作发生
    """
    if created:
        # 图片下载量加1
        image = instance.image
        image.download_nums += 1
        image.save()
        # 用户总图片下载量加1
        user = image.user
        user.download_nums += 1
        user.save()
