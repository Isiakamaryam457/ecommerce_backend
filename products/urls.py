from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    CategoryListCreateView,
    CategoryDetailView,
    ReviewListCreateView,
    ReviewDetailView,
    ProductImageListCreateView,
    ProductImageDetailView,
    WishlistView,
    WishlistAddProductView,
    WishlistRemoveProductView,
    OrderListCreateView,
    OrderDetailView
    )

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-details'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:product_pk>/reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('<int:product_pk>/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('<int:product_pk>/images/', ProductImageListCreateView.as_view(), name='image-list'),
    path('<int:product_pk>/images/<int:pk>/', ProductImageDetailView.as_view(), name='image-detail'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:product_pk>/', WishlistAddProductView.as_view(), name='wishlist-add'),
    path('wishlist/remove/<int:product_pk>/', WishlistRemoveProductView.as_view(), name='wishlist-remove'),
     path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]