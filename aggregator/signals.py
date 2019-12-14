from django.db.models.signals import post_save
from django.dispatch import receiver

from aggregator import models
from aggregator.tasks import telegram_notifications


@receiver(post_save, sender=models.Lot)
def lot_post_save(sender, instance, created, **kwargs):
    if created is True:
        # todo: сначала отправляем в сфинкс, что бы после в таске искать
        telegram_notifications.delay(instance.pk)
