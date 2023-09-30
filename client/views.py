from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from client.forms import ClientForm
from client.models import MailClient


class ClientListView(LoginRequiredMixin, ListView):
    model = MailClient
    template_name = 'mailclient_list.html'
    paginate_by = 10
    ordering = None

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset.order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = MailClient


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MailClient
    form_class = ClientForm
    permission_required = 'client.add_mailclient'
    success_url = reverse_lazy('client:list_clients')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Клиент успешно создан.')
        return super().form_valid(form)

    def form_invalid(self, form):
        if 'email' in form.errors and 'client_exists' in form.errors['email']:
            messages.error(self.request, 'Такой клиент уже существует.')
        return super().form_invalid(form)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailClient
    success_url = reverse_lazy('client:list_clients')
    permission_required = 'client.delete_mailclient'


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailClient
    form_class = ClientForm
    permission_required = 'client.change_mailclient'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('client:view_client', kwargs={'pk': self.object.pk})

