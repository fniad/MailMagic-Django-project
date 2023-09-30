from django.core.cache import cache
import random
from client.models import MailClient
from config import settings
from mailing.models import MailingSettings
from post.models import Post


def get_count_all_mailing_cache():
    if settings.CACHE_ENABLED:
        key = 'count_all_mailing'
        count_all_mailing = cache.get(key)
        if count_all_mailing is None:
            count_all_mailing = MailingSettings.objects.all().count()
            cache.set(key, count_all_mailing)
        else:
            count_all_mailing = MailingSettings.objects.all().count()
        return count_all_mailing


def get_count_started_mailing_cache():
    if settings.CACHE_ENABLED:
        key = 'count_started_mailing'
        count_started_mailing = cache.get(key)
        if count_started_mailing is None:
            count_started_mailing = MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED).count()
            cache.set(key, count_started_mailing)
        else:
            count_started_mailing = MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED).count()
        return count_started_mailing


def get_unique_clients_cache():
    if settings.CACHE_ENABLED:
        key = 'unique_clients'
        unique_clients = cache.get(key)
        if unique_clients is None:
            unique_clients = MailClient.objects.values('email').distinct().count()
            cache.set(key, unique_clients)
        else:
            unique_clients = MailClient.objects.values('email').distinct().count()
        return unique_clients


def get_all_articles_cache():
    if settings.CACHE_ENABLED:
        key = 'all_articles'
        all_articles = cache.get(key)
        if all_articles is None:
            all_articles = Post.objects.all()
            cache.set(key, all_articles)
        else:
            all_articles = Post.objects.all()
        return all_articles


def increase_views_count_for_random_articles(all_articles):
    num_articles_to_display = min(3, len(all_articles))
    articles = random.sample(list(all_articles), num_articles_to_display)

    for article in articles:
        article.views_count += 1
        article.save()


def get_random_articles(num_articles, all_articles):
    num_articles_to_display = min(num_articles, len(all_articles))
    articles = random.sample(list(all_articles), num_articles_to_display)
    return articles
