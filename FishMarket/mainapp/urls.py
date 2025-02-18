from django.urls import path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('products/<slug:slug>', views.ProductDetailView.as_view(), name='product'),
    path('categories-all-products/', views.AllProductsOrSpecificView.as_view(), name='AllProducts'),
]
