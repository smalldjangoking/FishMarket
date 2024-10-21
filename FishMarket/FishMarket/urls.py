from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('usersapp.urls', namespace='usersapp')),
    path('', include('mainapp.urls', namespace='mainapp')),
]
