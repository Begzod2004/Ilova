from django.urls import path
from .views import  ChatListView, ChatCreateView



urlpatterns = [
    path('chat/list/', ChatListView.as_view()),
    path('chat/create/', ChatCreateView.as_view()),
]
