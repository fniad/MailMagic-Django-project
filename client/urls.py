from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import ClientListView, ClientDetailView, ClientCreateView, ClientDeleteView, ClientUpdateView

app_name = ClientConfig.name

urlpatterns = [
    path('clients/', cache_page(60)(ClientListView.as_view()), name='list_clients'),
    path('view/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='view_client'),
    path('create/', ClientCreateView.as_view(), name='create_client'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
]
