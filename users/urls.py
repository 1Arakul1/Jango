from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # Добавлено редактирование профиля
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
]