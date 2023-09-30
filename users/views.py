from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserProfileForm, UserAuthenticationForm, ResetPasswordForm
from users.models import User
from users.services import create_vrf_token_or_random_password, send_confirm_url_vrf, send_generation_password


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'users/login.html'
    success_url = 'mailing:index'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_class(self):
        return self.authentication_form or self.form_class


class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False

        group = Group.objects.get(name='users')
        user.groups.set([group])

        vrf_token = create_vrf_token_or_random_password()
        confirm_url = self.request.build_absolute_uri(reverse('users:confirm', args=[vrf_token]))
        user.vrf_token = vrf_token

        user.save()

        send_confirm_url_vrf(confirm_url, user.email)

        return super().form_valid(form)


class ConfirmRegistrationView(View):
    def get(self, request, vrf_token):
        try:
            user = User.objects.get(vrf_token=vrf_token)
            user.is_active = True
            user.vrf_token = None
            user.save()
        except User.DoesNotExist:
            messages.error(request,
                           "Ошибка: Пользователь с указанным токеном не найден. Пройдите регистрацию снова.")
        return redirect('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def generate_new_password(request):
    new_password = create_vrf_token_or_random_password()

    send_generation_password(new_password, email=request.user.email)

    request.user.set_password(new_password)
    request.user.save()

    return redirect(reverse('mailing:index'))


def reset_password(request):
    """Сгенерировать новый пароль для пользователя если пароль забыли"""
    form = ResetPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user_email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=user_email)
            new_password = create_vrf_token_or_random_password()
            user.set_password(new_password)
            user.save()
            send_generation_password(new_password, user_email)
            return redirect(reverse("users:login"))
        except User.DoesNotExist:
            return render(request, 'users/change_password.html',
                          {'error_message': 'Пользователь не найден.'})
    return render(request, 'users/change_password.html', {'form': form})


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    paginate_by = 10
    permission_required = 'users.view_user'
    ordering = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj

        return context


@login_required
def toggle_status(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        profile = User.objects.get(id=object_id)
        profile.is_active = not profile.is_active
        profile.save()

        return redirect('users:users_list')

    return redirect('users:users_list')
