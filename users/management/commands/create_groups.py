from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание групп и назначение прав'

    def handle(self, *args, **options):
        # Создание группы модераторов
        moderators, created = Group.objects.get_or_create(name='moderators')
        bloggers, created = Group.objects.get_or_create(name='bloggers')
        users, created = Group.objects.get_or_create(name='users')

        moderators.is_staff = True
        moderators.save()
        bloggers.is_staff = True
        bloggers.save()

        post_content_type = ContentType.objects.get(app_label='post', model='post')
        mailingsettings_content_type = ContentType.objects.get(app_label='mailing', model='mailingsettings')
        mailingmessage_content_type = ContentType.objects.get(app_label='mailing', model='mailingmessage')
        mailinglog_content_type = ContentType.objects.get(app_label='mailing', model='mailinglog')
        mailclient_content_type = ContentType.objects.get(app_label='client', model='mailclient')
        user_content_type = ContentType.objects.get(app_label='users', model='user')

        # рассылки
        change_mailingsettings = Permission.objects.get(codename='change_mailingsettings',
                                                        content_type=mailingsettings_content_type)
        view_mailingsettings = Permission.objects.get(codename='view_mailingsettings',
                                                      content_type=mailingsettings_content_type)
        delete_mailingsettings = Permission.objects.get(codename='delete_mailingsettings',
                                                        content_type=mailingsettings_content_type)
        add_mailingsettings = Permission.objects.get(codename='add_mailingsettings',
                                                     content_type=mailingsettings_content_type)
        # письма из рассылок
        change_mailingmessage = Permission.objects.get(codename='change_mailingmessage',
                                                      content_type=mailingmessage_content_type)
        view_mailingmessage = Permission.objects.get(codename='view_mailingmessage',
                                                    content_type=mailingmessage_content_type)
        add_mailingmessage = Permission.objects.get(codename='add_mailingmessage',
                                                   content_type=mailingmessage_content_type)
        delete_mailingmessage = Permission.objects.get(codename='delete_mailingmessage',
                                                      content_type=mailingmessage_content_type)
        # логи рассылок
        view_mailinglog = Permission.objects.get(codename='view_mailinglog', content_type=mailinglog_content_type)
        # клиенты
        change_mailclient = Permission.objects.get(codename='change_mailclient', content_type=mailclient_content_type)
        view_mailclient = Permission.objects.get(codename='view_mailclient', content_type=mailclient_content_type)
        delete_mailclient = Permission.objects.get(codename='delete_mailclient', content_type=mailclient_content_type)
        add_mailclient = Permission.objects.get(codename='add_mailclient', content_type=mailclient_content_type)
        # статьи в блоге
        change_post = Permission.objects.get(codename='change_post', content_type=post_content_type)
        add_post = Permission.objects.get(codename='add_post', content_type=post_content_type)
        view_post = Permission.objects.get(codename='view_post', content_type=post_content_type)
        delete_post = Permission.objects.get(codename='delete_post', content_type=post_content_type)
        # пользователи
        change_user = Permission.objects.get(codename='change_user', content_type=user_content_type)
        view_user = Permission.objects.get(codename='view_user', content_type=user_content_type)

        #
        moderators.permissions.set(
            [
                view_mailingsettings, view_mailclient, view_mailinglog, view_mailingmessage, view_post,
                view_user, change_user
            ]
        )
        bloggers.permissions.set(
            [change_post, add_post, delete_post, view_post]
        )
        users.permissions.set(
            [
                add_mailingsettings, change_mailingsettings, view_mailingsettings, delete_mailingsettings,
                add_mailingmessage, change_mailingmessage, view_mailingmessage, delete_mailingmessage,
                add_mailclient, change_mailclient, view_mailclient, delete_mailclient, view_mailinglog,
                view_post
            ]
        )

        self.stdout.write(self.style.SUCCESS('Группы успешно созданы.'))
