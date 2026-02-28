from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    CategoryListCreateView,
    CategoryDetailView,
    ReviewListCreateView,
    ReviewDetailView
    )

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-details'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:product_pk>/reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('<int:product_pk>/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

]