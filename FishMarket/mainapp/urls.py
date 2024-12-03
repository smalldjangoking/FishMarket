from django.urls import path
from mainapp import views
from usersapp.urls import app_name

app_name = 'mainapp'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('products/<slug:slug>', views.ProductDetailView.as_view(), name='product'),
    path('categories/', views.CategoryListView.as_view(), name='Categories'),
    path('categories/<slug:slug>', views.CategorySelectView.as_view(), name='CategorySelect'),
    path('categories-all-products/', views.AllProductsOrSpecificView.as_view(), name='AllProducts'),
    path('delivery/', views.delivery, name='delivery'),
    path('about/', views.about, name='about'),
]
