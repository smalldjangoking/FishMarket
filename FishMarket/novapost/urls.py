from django.urls import path
from novapost import views

app_name = 'novapost'

urlpatterns = [
    path('db/get_city/', views.get_city, name='get_city'),
    path('db/get_warehouses', views.get_warehouses, name='get_warehouses'),
]