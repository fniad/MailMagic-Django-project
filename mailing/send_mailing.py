"""
Реализация рассылки писем
"""
import os
from datetime import datetime, timedelta
from smtplib import SMTPRecipientsRefused, SMTPException

import django
import dotenv
import pytz
from decouple import config
from django.core.mail import send_mail
from email_validator import validate_email, EmailNotValidError

dotenv.load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from mailing.models import MailingSettings, MailingLog, MailingMessage


def send_mails():
    """Рассылка писем"""
    desired_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now().astimezone(desired_timezone)
    current_time = now.time()
    time_window = timedelta(minutes=10)
    current_datetime = datetime.combine(datetime.today(), current_time)

    for mailing_settings in MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED):
        for mailing_client in mailing_settings.clients.all():
            start_datetime = current_datetime
            end_datetime = datetime.combine(datetime.today(), mailing_settings.time) + time_window

            if start_datetime <= end_datetime:
                last_try_date = get_last_try_date(mailing_client, mailing_settings, desired_timezone)
                mailing_message = get_mailing_message(mailing_settings)

                if has_successful_attempts(mailing_settings, now, last_try_date):
                    send_mail_if_eligible(mailing_client, mailing_message,
                                          mailing_settings, now, last_try_date, desired_timezone)
                else:
                    send_email(mailing_client, mailing_message, mailing_settings, desired_timezone)


def get_last_try_date(mailing_client, mailing_settings, desired_timezone):
    """Запрос БД: есть ли логи по рассылке.
    Если есть, то вернуть время последнего лога"""
    last_try = MailingLog.objects.filter(client=mailing_client,
                                         mailing_settings=mailing_settings).order_by('-sent_datetime').first()
    if last_try:
        return last_try.sent_datetime.astimezone(desired_timezone)
    return None


def get_mailing_message(mailing_settings):
    """Запрос из БД данных о письме конкретной рассылки"""
    return MailingMessage.objects.filter(mailing=mailing_settings).first()


def has_successful_attempts(mailing_settings, now, last_try_date):
    """Проверка, прошло ли достаточно времени для следующей отправки"""
    eligible = False

    if last_try_date:
        if mailing_settings.PERIOD_DAILY:
            eligible = (now.date() - last_try_date.date()).days >= 1
        elif mailing_settings.PERIOD_WEEKLY:
            eligible = (now.date() - last_try_date.date()).days >= 7
        elif mailing_settings.PERIOD_MONTHLY:
            eligible = (now.date() - last_try_date.date()).days >= 30

    return eligible


def send_mail_if_eligible(mailing_client, mailing_message, mailing_settings, now, last_try_date, desired_timezone):
    """Вызов send_email, если подошло время"""
    eligible = has_successful_attempts(mailing_settings, now, last_try_date)

    if eligible:
        send_email(mailing_client, mailing_message, mailing_settings, desired_timezone)


def send_email(mailing_client, mailing_message, mailing, desired_timezone):
    """Отправка письма и создание лога об этом"""
    subject = mailing_message.subject
    message = mailing_message.body
    from_email = config('EMAIL_HOST_USER')
    recipient_list = [mailing_client.email]

    now = datetime.now().astimezone(desired_timezone)

    for recipient in recipient_list:
        try:
            if validate_email(recipient):
                try:
                    success_count = send_mail(
                        subject=subject,
                        message=message,
                        from_email=from_email,
                        recipient_list=[recipient],
                        fail_silently=False,
                    )
                    if success_count == 0:
                        status = MailingLog.STATUS_FAIL
                        server_response = "ошибка при отправке письма"
                    else:
                        status = MailingLog.STATUS_OK
                        server_response = 'отправлено'
                except (SMTPRecipientsRefused, SMTPException) as e:
                    status = MailingLog.STATUS_FAIL
                    server_response = str(e)
        except EmailNotValidError:
            status = MailingLog.STATUS_FAIL
            server_response = 'недействительный email'

        mailing_log = create_mailing_log(mailing_client, mailing, now, status, server_response)
        mailing_log.mailing_settings_str = mailing.mailing_name
        mailing_log.save()


def create_mailing_log(client, mailing_settings, sent_datetime, status, server_response):
    """Создание и возврат объекта MailingLog"""
    mailing_log = MailingLog.objects.create(
        client=client,
        sent_datetime=sent_datetime,
        status=status,
        server_response=server_response
    )
    mailing_log.mailing_settings.set([mailing_settings])
    return mailing_log


if __name__ == '__main__':
    send_mails()
