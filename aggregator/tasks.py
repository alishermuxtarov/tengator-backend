from tengator.celery import app as celery_app
from django.conf import settings
from aggregator import utils


@celery_app.task()
def lot_post_save(pk):
    from aggregator import models

    instance = models.Lot.objects.get(pk=pk)

    text = ''
    for f in instance.files.all():
        text += utils.get_text_from_file(f.file.path)

    models.FtsTengator.objects.update_record(
        id=instance.pk,
        title=instance.title,
        description=instance.description,
        files=text
    )

    if settings.DEBUG is True:
        search_words(instance.pk)
    else:
        search_words.delay(instance.pk)


@celery_app.task()
def search_words(lot_id):
    from aggregator import models

    for obj in models.SearchWord.objects.all():
        result = models.FtsTengator.objects.search(obj.word, pk=lot_id)
        if result:
            for pk in result:
                o = models.Lot.objects.get(pk=pk)
                if settings.DEBUG is True:
                    telegram_notifications(obj.word, o.url, obj.user.uid)
                else:
                    telegram_notifications.delay(obj.word, o.url, obj.user.uid)


@celery_app.task()
def telegram_notifications(word, url, uid):
    import telebot

    bot = telebot.TeleBot(token=settings.TOKEN)
    bot.send_message(uid, '''Найдено совпадение по слову: {}. 
Посмотреть лот можно по ссылке: {}'''.format(word, url))
