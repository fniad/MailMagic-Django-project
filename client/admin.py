from django.contrib import admin

from client.models import MailClient


@admin.register(MailClient)
class MailClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment', 'owner',)
    list_filter = ('full_name', 'email', 'owner',)
    search_fields = ('full_name', 'email', 'owner',)
