from django.urls import path
from . import views

urlpatterns = [
    path('', views.blindbox_list, name='blindbox_list'),
    path('create/', views.create_blindbox, name='create_blindbox'),
    path('<int:pk>/open/', views.open_blindbox, name='open_blindbox'),
]