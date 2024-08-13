from django.urls import path
from . import views
from django.conf import settings
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductVersionCreateView, ProductVersionDeleteView, ProductVersionListView, ProductVersionUpdateView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('products/', views.IndexView.as_view(), name='index'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('create_product/', views.ProductCreateView.as_view(), name='create_product'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('blog/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/delete/', views.BlogPostDeleteView.as_view(), name='blog_delete'),
    path('blog/', views.BlogPostListView.as_view(), name='blogpost_list'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blog/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product-version/', ProductVersionListView.as_view(), name='product_version_list'),
    path('product-version/create/', ProductVersionCreateView.as_view(), name='product_version_create'),
    path('product-version/<int:pk>/edit/', ProductVersionUpdateView.as_view(), name='product_version_edit'),
    path('product-version/<int:pk>/delete/', ProductVersionDeleteView.as_view(), name='product_version_delete'),
]
