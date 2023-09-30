from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from mailing.models import NULLABLE


class User(AbstractUser):
    DoesNotExist = ObjectDoesNotExist
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    vrf_token = models.CharField(max_length=12, verbose_name='токен', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активный')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
