from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, generate_new_password, ConfirmRegistrationView, reset_password, \
    UserListView, toggle_status

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('confirm/<str:vrf_token>/', ConfirmRegistrationView.as_view(), name='confirm'),
    path('reset_password/', reset_password, name='reset_password'),
    path('users/', UserListView.as_view(), name='users_list'),
    path('toggle_status/', toggle_status, name='toggle_status'),
]
