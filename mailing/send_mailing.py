import os
import django
import dotenv
dotenv.load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from smtplib import SMTPException, SMTPRecipientsRefused
from datetime import datetime, timedelta
import pytz
from decouple import config
from django.core.mail import send_mail
from mailing.models import MailingSettings, MailingLog, MailingMessage


def send_mails():
    desired_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now().astimezone(desired_timezone)
    current_time = now.time()
    time_window = timedelta(minutes=10)
    current_datetime = datetime.combine(datetime.today(), current_time)

    for mailing in MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED):
        for mailing_client in mailing.clients.all():

            start_datetime = current_datetime
            end_datetime = datetime.combine(datetime.today(), mailing.time) + time_window

            if start_datetime <= end_datetime:
                mailing_log = MailingLog.objects.filter(client=mailing_client, mailing_settings=mailing)
                mailing_message = MailingMessage.objects.filter(mailing=mailing).first()

                if mailing_log.exists():
                    last_try = mailing_log.order_by('-sent_datetime').first()
                    last_try_date = last_try.sent_datetime.astimezone(desired_timezone)
                    if mailing.PERIOD_DAILY:
                        if (now.date() - last_try_date.date()).days >= 1:
                            send_email(mailing_client, mailing_message, mailing)
                    elif mailing.PERIOD_WEEKLY:
                        if (now.date() - last_try_date.date()).days >= 7:
                            send_email(mailing_client, mailing_message, mailing)
                    elif mailing.PERIOD_MONTHLY:
                        if (now.date() - last_try_date.date()).days >= 30:
                            send_email(mailing_client, mailing_message, mailing)
                else:
                    send_email(mailing_client, mailing_message, mailing)


def send_email(mailing_client, mailing_message, mailing):
    subject = mailing_message.subject
    message = mailing_message.body
    from_email = config('EMAIL_HOST_USER')
    recipient_list = [mailing_client.email]

    desired_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.now().astimezone(desired_timezone)
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        mailing_log = MailingLog.objects.create(
            client=mailing_client,
            sent_datetime=now,
            status=MailingLog.STATUS_OK,
            server_response='отправлено'
        )
        mailing_log.mailing_settings.set([mailing])
        mailing_log.mailing_settings_str = mailing.mailing_name
        mailing_log.save()
    except (SMTPException, SMTPRecipientsRefused) as e:
        mailing_log = MailingLog.objects.create(
            client=mailing_client,
            mailing_settings=mailing,
            sent_datetime=now,
            status=MailingLog.STATUS_FAIL,
            server_response=str(e)
        )
        mailing_log.mailing_settings.set([mailing])
        mailing_log.mailing_settings_str = mailing.mailing_name
        mailing_log.save()


if __name__ == '__main__':
    send_mails()
