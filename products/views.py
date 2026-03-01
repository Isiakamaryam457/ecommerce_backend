from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Product, Category, Review, ProductImage, Wishlist, Order, OrderItem, Discount
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer, WishlistSerializer, OrderItemSerializer, OrderSerializer, DiscountSerializer
from .filters import ProductFilter 

# List all products or create a new one
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # only authenticated users can create
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'category__name'] # search by name or category
    ordering_fields = ['price', 'created_date']  # order by price or date
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # auto-assign the logged in user


# Get, Update, Delete a single product
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# List all categories or create a new one
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']  # search categories by name or description
    ordering_fields = ['name', 'created_date']

    def get_queryset(self):
        # by default only show active categories
        show_all = self.request.query_params.get('show_all', None)
        if show_all and self.request.user.is_staff:  # only admin can see inactive
            return Category.objects.all()
        return Category.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # auto assign creator



# Get, Update, Delete a single category
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        # soft delete - instead of deleting, just mark as inactive
        instance.is_active = False
        instance.save()


# Review views
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])  # only reviews for this product

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        # check if user already reviewed this product
        if Review.objects.filter(product=product, user=self.request.user).exists():
            raise ValidationError("You have already reviewed this product.")
        serializer.save(user=self.request.user, product=product)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

# Product Image views
class ProductImageListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        serializer.save(product=product)

class ProductImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])

# Wishlist views
class WishlistView(generics.RetrieveAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

    def get_object(self):
        # get or create wishlist for the logged in user automatically
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        return wishlist

class WishlistAddProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_pk):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=product_pk)

        if wishlist.products.filter(pk=product_pk).exists():
            return Response(
                {'detail': 'Product already in wishlist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        wishlist.products.add(product)
        return Response(
            {'detail': f'{product.name} added to wishlist.'},
            status=status.HTTP_200_OK
        )

class WishlistRemoveProductView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_pk):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=product_pk)

        if not wishlist.products.filter(pk=product_pk).exists():
            return Response(
                {'detail': 'Product not in wishlist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        wishlist.products.remove(product)
        return Response(
            {'detail': f'{product.name} removed from wishlist.'},
            status=status.HTTP_200_OK
        )

# Order views
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # users only see their own orders

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        order = self.get_object()
        new_status = self.request.data.get('status')

        # restore stock if order is cancelled
        if new_status == 'cancelled' and order.status != 'cancelled':
            for item in order.items.all():
                item.product.restore_stock(item.quantity)

        serializer.save()

# Discount views
class DiscountListCreateView(generics.ListCreateAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Discount.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        serializer.save(created_by=self.request.user, product=product)

class DiscountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Discount.objects.filter(product_id=self.kwargs['product_pk'])
