from django.urls import path
from mainapp import views
from usersapp.urls import app_name

app_name = 'mainapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('delivery/', views.delivery, name='delivery'),
    path('about/', views.about, name='about'),
]
