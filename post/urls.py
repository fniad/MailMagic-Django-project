from django.urls import path
from django.views.decorators.cache import cache_page

from post.apps import BlogConfig
from post.views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create_article'),
    path('', cache_page(60)(PostListView.as_view()), name='list_articles'),
    path('view/<int:pk>/', cache_page(60)(PostDetailView.as_view()), name='view_article'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='edit_article'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete_article'),
]
