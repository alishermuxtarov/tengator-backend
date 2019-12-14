from django.db.models.signals import post_delete
from django.dispatch import receiver

from aggregator import models


@receiver(post_delete, sender=models.Lot)
def lot_post_delete(sender, instance, **kwargs):
    models.FtsTengator.objects.delete_record(instance.id)

