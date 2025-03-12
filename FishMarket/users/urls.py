from django.contrib.auth.views import PasswordChangeView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from FishMarket.helpers import user_not_authenticated
from .forms import CustomAuthenticationForm, UserPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from .views import UserView, signup, user_addresses, user_order_history, email_confirmed, \
    email_confirmation, user_profile_email_confirm, email_send_repeat

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',
                                                authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
    path('profile/', login_required(UserView.as_view()), name='profile'),
    path('signup/', signup, name='signup'),
    path('profile/addresses/', user_addresses, name='user_addresses'),
    path('profile/history/', user_order_history, name='user_history'),
    path('profile/confirm-email/', user_profile_email_confirm, name='user_create_confirm'),
    path('password-change/', login_required(PasswordChangeView.as_view(form_class=UserPasswordChangeForm,
                                                                       success_url=reverse_lazy(
                                                                           "users:password_change_done"),
                                                                       template_name=
                                                                       "users/password_change_form.html")),
         name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/', user_not_authenticated(auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                                                 email_template_name='users/password_reset_email.html',
                                                                 form_class=CustomPasswordResetForm,
                                                                 success_url=reverse_lazy(
                                                                     "users:password_reset_done"),
                                                                 )),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                     success_url=reverse_lazy('users:password_reset_complete'),
                                                     form_class=CustomSetPasswordForm),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('email-comfirm/', email_confirmation, name='email_confirm'),
    path('email-confirmed/<token>/', email_confirmed, name='email-confirmed'),
    path('profile-confirm-email/', email_send_repeat, name='send-user-confirm-again'),

]
