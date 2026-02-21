from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # shows full category details on read
    category_id = serializers.PrimaryKeyRelatedField(  # accepts category id on write
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 
            'category', 'category_id', 'stock_quantity',
            'image_url', 'created_date'
        ]
        read_only_fields = ['created_date']