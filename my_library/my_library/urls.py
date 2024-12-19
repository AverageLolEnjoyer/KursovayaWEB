from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
