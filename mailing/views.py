from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from mailing.forms import MailingSettingsForm, MailingMessageForm
from mailing.models import MailingSettings, MailingMessage, MailingLog
from mailing.services import get_count_all_mailing_cache, get_count_started_mailing_cache, get_unique_clients_cache, \
    get_all_articles_cache, increase_views_count_for_random_articles, get_random_articles


def index(request):
    mailing_count = get_count_all_mailing_cache()
    mailing_active_count = get_count_started_mailing_cache()
    count_unique_clients = get_unique_clients_cache()
    all_articles = get_all_articles_cache()

    increase_views_count_for_random_articles(all_articles)

    context = {
        'mailing_count': mailing_count,
        'mailing_active_count': mailing_active_count,
        'count_unique_clients': count_unique_clients,
        'articles': get_random_articles(3, all_articles),
    }

    return render(request, 'mailing/index.html', context)


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingSettings
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


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MailingSettings
    permission_required = 'mailing.add_mailingsettings'
    success_url = reverse_lazy('mailing:list_mailing')
    form_class = MailingSettingsForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingMessageFormset = inlineformset_factory(MailingSettings, MailingMessage, form=MailingMessageForm, extra=1)
        if self.request.method == 'POST':
            formset = MailingMessageFormset(self.request.POST)
        else:
            formset = MailingMessageFormset()

        context_data['formset'] = formset
        return context_data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_superuser:
            mailing_owner = self.request.POST.get('owner', None) if self.request.method == 'POST' else None
            kwargs['user'] = mailing_owner
        else:
            kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user

            formset.instance = self.object
            self.object.save()
            formset.save()

            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingMessageFormset = inlineformset_factory(MailingSettings, MailingMessage, form=MailingMessageForm, extra=1)
        if self.request.method == 'POST':
            formset = MailingMessageFormset(self.request.POST, instance=self.object)
        else:
            formset = MailingMessageFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:list_mailing')
    permission_required = 'mailing.delete_mailingsettings'


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    permission_required = 'mailing.change_mailingsettings'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('mailing:view_mailing', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_superuser:
            mailing_owner = self.request.POST.get('owner', None) if self.request.method == 'POST' else None
            kwargs['user'] = mailing_owner
        else:
            kwargs['user'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingMessageFormset = inlineformset_factory(MailingSettings, MailingMessage, form=MailingMessageForm, extra=1)
        if self.request.method == 'POST':
            formset = MailingMessageFormset(self.request.POST, instance=self.object)
        else:
            formset = MailingMessageFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            if self.request.user.groups.filter(name='users').exists():
                self.object.owner = self.request.user

            formset.instance = self.object
            self.object.save()
            formset.save()

            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    paginate_by = 10
    ordering = None

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset.order_by('sent_datetime')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context


class MailingLogDetailView(LoginRequiredMixin, DetailView):
    model = MailingLog
