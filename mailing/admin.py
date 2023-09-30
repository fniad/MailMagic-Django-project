from django.contrib import admin
from mailing.models import MailingMessage, MailingLog, MailingSettings


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'subject', 'body',)
    list_filter = ('mailing', 'subject',)
    search_fields = ('mailing',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('mailing_name', 'time', 'period', 'status',  'owner',)
    list_filter = ('mailing_name', 'period', 'status',  'owner',)
    search_fields = ('mailing_name',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('mailing_settings_str', 'client', 'status', 'sent_datetime', 'owner',)
    list_filter = ('status', 'mailing_settings_str', 'sent_datetime', 'owner',)
    search_fields = ('mailing_settings_str', 'owner',)
