from django.contrib import admin

from post.models import Post


@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'is_published')
    search_fields = ('title', 'body')
