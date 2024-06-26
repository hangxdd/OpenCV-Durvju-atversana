from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users/', views.users_view, name='users_view'),
    path('about/', views.about_view, name='about_view'),
    path('edit_user/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('delete_image/<int:user_id>/<str:image_name>/', views.delete_image_view, name='delete_image'),
    path('add_user/', views.add_user_view, name='add_user'),
]