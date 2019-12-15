from hashlib import md5

from django.utils.translation import ugettext as _
from django.db import models
from textract import process


def get_text_from_file(filename):
    try:
        return process(filename).decode('utf-8')
    except:
        return ''


def md5_text(text):
    return md5(text.encode('utf-8')).hexdigest()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name=_('Время создания'))
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True, verbose_name=_('Время обновления'))
    created_by = models.ForeignKey('aggregator.User', models.CASCADE, null=True, blank=True,
                                   related_name='created_%(app_label)s_%(model_name)ss', editable=False,
                                   verbose_name=_('Создано пользователем'))

    class Meta:
        abstract = True
        ordering = ('id',)
        get_latest_by = 'created_at'
