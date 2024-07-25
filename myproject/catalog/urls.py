from django.urls import path
from . import views
from myproject import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
]
