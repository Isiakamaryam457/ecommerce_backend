from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # shows username instead of id

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_date']
        read_only_fields = ['created_date']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # shows full category details on read
    category_id = serializers.PrimaryKeyRelatedField(  # accepts category id on write
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    reviews = ReviewSerializer(many=True, read_only=True)  # shows all reviews on product
    average_rating = serializers.SerializerMethodField()   # shows average rating



    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 
            'category', 'category_id', 'stock_quantity',
            'image_url', 'created_date', 'reviews', 'average_rating'
        ]
        read_only_fields = ['created_date']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None