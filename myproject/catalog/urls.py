from django.urls import path
from . import views
from django.conf import settings

from myproject import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
]
