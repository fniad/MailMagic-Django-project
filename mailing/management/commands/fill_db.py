from django.core.management import BaseCommand
from django.core.management import call_command
from mailing.models import MailingSettings, MailingLog, MailingMessage
from client.models import MailClient
from post.models import Post


class Command(BaseCommand):
    help = 'Удалить все объекты из БД.'

    def handle(self, *args, **options):
        MailingMessage.objects.all().delete()
        MailClient.objects.all().delete()
        MailingLog.objects.all().delete()
        MailingSettings.objects.all().delete()
        MailClient.objects.all().delete()
        Post.objects.all().delete()

        call_command('loaddata', 'fixtures/data.json')

        self.stdout.write(self.style.SUCCESS('Объекты были удалены из БД'))
