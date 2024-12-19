from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_book, name='add_book'),
    path('add-borrowed/', views.add_borrowed_book, name='add_borrowed_book'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),  # Добавьте этот маршрут
    path('register/', views.register, name='register'),  # маршрут для регистрации
    path('students/', views.student_list, name='student_list'),
    path('delete-borrowed/<int:borrowed_book_id>/', views.delete_borrowed_book, name='delete_borrowed_book'),
    path('search/', views.search_book, name='search_book'),  # Новый маршрут для поиска
]
