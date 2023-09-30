from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingListView, index, MailingCreateView, MailingUpdateView, MailingDetailView, \
    MailingDeleteView, MailingLogListView, MailingLogDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('mailing/', cache_page(60)(MailingListView.as_view()), name='list_mailing'),
    path('', index, name='index'),
    path('create/', MailingCreateView.as_view(), name='create_mailing'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('view/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='view_mailing'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('mailing-log/', cache_page(60)(MailingLogListView.as_view()), name='list_mailing_log'),
    path('mailing-log/<int:pk>/', cache_page(60)(MailingLogDetailView.as_view()), name='view_mailing_log'),
]
