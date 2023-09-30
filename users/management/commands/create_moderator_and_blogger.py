from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from users.models import User
from decouple import config


class Command(BaseCommand):
    help = 'Добавляем в соответствующие группы модератора и ответственного за блог'

    def handle(self, *args, **options):
        moderator = User.objects.create(
            email=config('MODERATOR_EMAIL'),
            first_name='Moderator',
            last_name='MailMagic',
            is_staff=True,
            is_superuser=False,
        )

        blogger = User.objects.create(
            email=config('BLOGGER_EMAIL'),
            first_name='Content-manager',
            last_name='MailMagic-blog',
            is_staff=True,
            is_superuser=False,
        )

        moderator.groups.add(Group.objects.get(name='moderators'))
        blogger.groups.add(Group.objects.get(name='bloggers'))

        moderator.set_password(config('MODERATOR_PASSWORD'))
        moderator.save()
        blogger.set_password(config('BLOGGER_PASSWORD'))
        blogger.save()

        self.stdout.write(self.style.SUCCESS('Контент-менеджер блога и модератор успешно добавлены.'))
