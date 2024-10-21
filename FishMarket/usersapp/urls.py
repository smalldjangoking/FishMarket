from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .forms import CustomAuthenticationForm
from .views import UserView, signup

app_name = 'usersapp'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usersapp/login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
    path('profile/', login_required(UserView.as_view()), name='profile'),
    path('signup/', signup, name='signup')
]

