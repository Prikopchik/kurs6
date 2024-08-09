from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('', views.index_view, name='index'),
    path('create/', views.create_product, name='create_product'),
    path('', views.create_product, name='create_product'),
    path('list/', views.product_list, name='product_list'),
    path('', views.product_list, name='product_list'),
]
