import imghdr
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ImageModel, GroupImage


@receiver(post_save, sender=ImageModel)
def create_group_image(sender, instance=None, created=False, **kwargs):
    """
    当上传图片动作发生
    """
    if created:
        # 保存图片格式
        pattern = imghdr.what(instance.image.path)
        instance.pattern = pattern
        instance.save()
        # 保存图片种类
        cates = instance.cates.split(" ")
        for cate in cates:
            if cate:
                GroupImage(image=instance, name=cate).save()
