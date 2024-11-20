import os
from django.db.models.signals import post_migrate, post_delete, pre_save
from django.dispatch import receiver

from core.models import Blogs


def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)


@receiver(pre_save, sender=Blogs)
def default_delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return

    if old_file != instance.image:
        if old_file:
            delete_file(old_file.path)
        return

@receiver(post_delete, sender=Blogs)
def default_delete_associated_image(sender, instance, **kwargs):
    if instance.image:
        delete_file(instance.image.path)