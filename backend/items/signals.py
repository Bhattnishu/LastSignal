from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import ItemReport


@receiver(post_delete, sender=ItemReport)
def delete_report_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)