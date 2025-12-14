from django.urls import path
from . import views

urlpatterns = [
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('create/<int:user_id>/', views.create_room, name='create_room'),
    path('room/<int:room_id>/send/', views.send_message, name='send_message'),
    path('unread_count/', views.unread_count, name='unread_count'),  # 未读消息检查
    path('mark_read/<int:room_id>/', views.mark_read, name='mark_read'),  # 标
]