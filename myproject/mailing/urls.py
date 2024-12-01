from django.urls import path
from . import views

urlpatterns = [
    path('recipients/', views.recipient_list, name='recipient_list'),
    path('recipients/<int:pk>/', views.recipient_detail, name='recipient_detail'),

    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/new/', views.message_create, name='message_create'),
    path('messages/<int:pk>/edit/', views.message_edit, name='message_edit'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),
    
    path('mailings/', views.mailing_list, name='mailing_list'),
    path('mailings/<int:pk>/', views.mailing_detail, name='mailing_detail'),
    path('mailings/new/', views.mailing_create, name='mailing_create'),
    path('mailings/<int:pk>/edit/', views.mailing_edit, name='mailing_edit'),
    path('mailings/<int:pk>/delete/', views.mailing_delete, name='mailing_delete'),
]
