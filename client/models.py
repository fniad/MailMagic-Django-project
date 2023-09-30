from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class MailClient(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(verbose_name='email')
    comment = models.TextField(max_length=500, verbose_name='комментарий', ** NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.email} ({self.full_name}) - {self.comment}'

    class Meta:
        verbose_name = 'клиент сервиса'
        verbose_name_plural = 'клиенты сервиса'
        unique_together = ('owner', 'email')
