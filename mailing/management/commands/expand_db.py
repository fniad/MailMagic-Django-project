from django.core import serializers
from django.core.management import BaseCommand
from itertools import chain

from post.models import Post
from client.models import MailClient
from mailing.models import MailingSettings, MailingLog, MailingMessage


class Command(BaseCommand):
    help = 'Перенос БД в json-файл'

    def handle(self, *args, **options):
        models = [Post, MailingMessage, MailingLog, MailingSettings, MailClient]

        with open('fixtures/data.json', 'w') as file:
            data = serializers.serialize('json', chain(*[model.objects.all() for model in models]))
            file.write(data)

        self.stdout.write(self.style.SUCCESS('Данные из БД успешно сохранены в data.json'))
