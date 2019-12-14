from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from aggregator import models
from aggregator.tasks import search_words


@receiver(post_save, sender=models.Lot)
def lot_post_save(sender, instance, created, **kwargs):
    if created is True:
        models.FtsTengator.objects.update_record(
            id=instance.pk,
            title=instance.title.replace("'", '"'),
            description=instance.description.replace("'", '"'),
        )
        if settings.DEBUG is True:
            search_words(instance.pk)
        else:
            search_words.delay(instance.pk)


@receiver(post_delete, sender=models.Lot)
def lot_post_delete(sender, instance, **kwargs):
    models.FtsTengator.objects.delete_record(instance.id)

