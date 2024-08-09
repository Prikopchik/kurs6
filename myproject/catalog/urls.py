from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('', views.index_view, name='index'),
]
