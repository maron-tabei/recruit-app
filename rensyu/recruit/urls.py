from django.urls import path
from . import views

urlpatterns = [
    path('', views.recruit_list, name='recruit_list'),
    path('create/', views.recruit_create, name='recruit_create'),
    path('edit/<int:pk>/', views.recruit_edit, name='recruit_edit'),
    path('delete/<int:pk>/', views.recruit_delete, name='recruit_delete'),
] 