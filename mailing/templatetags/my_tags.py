from django import template
from django.conf import settings

register = template.Library()


# <img src="{% mediapath object.image %}" />
@register.simple_tag
def mediapath(filepath):
    return f"{settings.MEDIA_URL}{filepath}"