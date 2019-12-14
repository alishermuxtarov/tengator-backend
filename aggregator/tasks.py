from tengator.celery import app as celery_app
from django.conf import settings


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
    from django.conf import settings
    import telebot

    bot = telebot.TeleBot(token=settings.TOKEN)
    bot.send_message(uid, '''Найдено совпадение по слову: {}. 
Посмотреть лот можно по ссылке: {}'''.format(word, url))
