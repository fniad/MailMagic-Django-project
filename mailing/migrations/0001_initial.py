# Generated by Django 4.2.3 on 2023-09-26 16:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_name', models.CharField(max_length=50, verbose_name='название рассылки')),
                ('time', models.TimeField(choices=[(datetime.time(0, 0), '00:00'), (datetime.time(1, 0), '01:00'), (datetime.time(2, 0), '02:00'), (datetime.time(3, 0), '03:00'), (datetime.time(4, 0), '04:00'), (datetime.time(5, 0), '05:00'), (datetime.time(6, 0), '06:00'), (datetime.time(7, 0), '07:00'), (datetime.time(8, 0), '08:00'), (datetime.time(9, 0), '09:00'), (datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00'), (datetime.time(23, 0), '23:00')], verbose_name='время')),
                ('period', models.CharField(choices=[('ежедневная', 'Ежедневная'), ('еженедельная', 'Раз в неделю'), ('ежемесячная', 'Раз в месяц')], max_length=20, verbose_name='периодичность')),
                ('status', models.CharField(choices=[('запущена', 'Запущена'), ('создана', 'Создана'), ('завершена', 'Завершена')], max_length=20, verbose_name='статус')),
                ('clients', models.ManyToManyField(to='client.mailclient', verbose_name='клиенты')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='заголовок письма')),
                ('body', models.TextField(verbose_name='тело письма')),
                ('mailing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailingsettings')),
            ],
            options={
                'verbose_name': 'письмо',
                'verbose_name_plural': 'письма',
            },
        ),
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_datetime', models.DateTimeField(auto_now_add=True, verbose_name='время')),
                ('status', models.CharField(choices=[('Успешно', 'Успешно'), ('Ошибка', 'Ошибка')], max_length=10, verbose_name='статус')),
                ('server_response', models.TextField(blank=True, verbose_name='ответ сервера')),
                ('mailing_settings_str', models.CharField(blank=True, max_length=50, verbose_name='название рассылки')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.mailclient', verbose_name='клиент')),
                ('mailing_settings', models.ManyToManyField(related_name='mailing_logs', to='mailing.mailingsettings', verbose_name='рассылка')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'логи рассылки',
                'verbose_name_plural': 'логи рассылок',
            },
        ),
    ]
