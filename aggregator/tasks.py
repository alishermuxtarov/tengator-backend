from tengator.celery import app as celery_app


@celery_app.task()
def telegram_notifications(lot_id):
    pass
