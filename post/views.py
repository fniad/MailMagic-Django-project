from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from post.forms import PostForm
from post.models import Post
from pytils.translit import slugify
from django.utils.text import slugify

from post.services import generate_unique_slug, increase_views_count


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    permission_required = 'post.add_post'
    success_url = reverse_lazy('post:list_articles')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save(commit=False)
            slug = slugify(new_article.title)
            new_article.slug = generate_unique_slug(slug)
            new_article.save()

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    permission_required = 'post.change_post'

    def get_success_url(self):
        return reverse_lazy('post:view_article', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.is_valid():
            updated_article = form.save(commit=False)
            if updated_article.title != form.initial['title'] or \
               updated_article.body != form.initial['body']:
                updated_article.slug = slugify(updated_article.title)
                updated_article.slug = generate_unique_slug(updated_article.slug)
                updated_article.save()

        return super().form_valid(form)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'
    paginate_by = 10
    ordering = None

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    # увеличение количества просмотров
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        increase_views_count(self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'post.delete_article'
    success_url = reverse_lazy('post:list_articles')
