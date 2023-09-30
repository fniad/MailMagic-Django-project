import random
import string
from django.core.mail import send_mail
from config import settings


def create_vrf_token_or_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(12))


def send_confirm_url_vrf(confirm_url, email):
    send_mail(
        subject='Поздравляем с регистрацией на сайте MailMagic',
        message=f'Пожалуйста, подтвердите свою электронную почту по ссылке {confirm_url}.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def send_generation_password(new_password, email):
    send_mail(
        subject='Вы сменили пароль на сайте MailMagic',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
