from django import forms

from mailing.forms import StyleFormMixin
from post.models import Post


class PostForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'preview_img')
