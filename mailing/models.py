from django.db import models
from datetime import time
from django.conf import settings

from client.models import MailClient

NULLABLE = {'blank': True, 'null': True}


class MailingSettings(models.Model):

    TIME = [(time(hour=i), time(hour=i).strftime('%H:00')) for i in range(24)]

    PERIOD_DAILY = 'ежедневная'
    PERIOD_WEEKLY = 'еженедельная'
    PERIOD_MONTHLY = 'ежемесячная'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'создана'
    STATUS_STARTED = 'запущена'
    STATUS_DONE = 'завершена'

    STATUSES = (
        (STATUS_STARTED, 'Запущена'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_DONE, 'Завершена'),
    )

    mailing_name = models.CharField(max_length=50, verbose_name='название рассылки')
    time = models.TimeField(choices=TIME, verbose_name='время')
    period = models.CharField(max_length=20, choices=PERIODS, verbose_name='периодичность')
    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='статус')
    clients = models.ManyToManyField(MailClient, verbose_name='клиенты')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f"{self.time} - {self.period} - {self.status}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=255, verbose_name='заголовок письма')
    body = models.TextField(verbose_name='тело письма')
    mailing = models.OneToOneField(MailingSettings, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class MailingLog(models.Model):

    STATUS_OK = 'Успешно'
    STATUS_FAIL = 'Ошибка'

    STATUS_CHOICES = [
        (STATUS_OK, 'Успешно'),
        (STATUS_FAIL, 'Ошибка'),
    ]

    client = models.ForeignKey(MailClient, on_delete=models.CASCADE, verbose_name='клиент')
    mailing_settings = models.ManyToManyField(MailingSettings, verbose_name='рассылка', related_name='mailing_logs')
    sent_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='статус')
    server_response = models.TextField(blank=True, verbose_name='ответ сервера')
    mailing_settings_str = models.CharField(max_length=50, blank=True, verbose_name='название рассылки')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.mailing_settings_str} - {self.sent_datetime}'

    class Meta:
        verbose_name = 'логи рассылки'
        verbose_name_plural = 'логи рассылок'
