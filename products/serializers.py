from rest_framework import serializers
from .models import Category, Product, Review, ProductImage, Wishlist, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)  # shows username
    product_count = serializers.SerializerMethodField()  # shows number of products in category

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_by', 'created_date', 'updated_date', 'is_active', 'product_count']
        read_only_fields = ['created_date', 'updated_date', 'created_by']


        def get_product_count(self, obj):
            return obj.products.count()  # counts products in this category


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'uploaded_date']
        read_only_fields = ['uploaded_date']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # shows username instead of id

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_date']
        read_only_fields = ['created_date',]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # shows full category details on read
    category_id = serializers.PrimaryKeyRelatedField(  # accepts category id on write
        queryset=Category.objects.filter(is_active=True),  # only active categories
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

class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  # shows full product details
    product_ids = serializers.PrimaryKeyRelatedField(  # accepts product ids to add
        queryset=Product.objects.all(),
        many=True,
        write_only=True,
        source='products'
    )
    total_items = serializers.SerializerMethodField()  # shows total items in wishlist

    class Meta:
        model = Wishlist
        fields = ['id', 'products', 'product_ids', 'total_items', 'created_date']
        read_only_fields = ['created_date']

    def get_total_items(self, obj):
        return obj.products.count()

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # shows full product details
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'total_price']
        read_only_fields = ['price']  # price is set automatically at time of purchase

    def get_total_price(self, obj):
        return obj.get_total_price()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  # nested order items
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items', 'total_price', 'created_date', 'updated_date']
        read_only_fields = ['total_price', 'created_date', 'updated_date']

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # extract items from data
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            # check stock before placing order
            if quantity > product.stock_quantity:
                order.delete()  # delete the order if stock is insufficient
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. Only {product.stock_quantity} available."
                )

            # create order item and lock in the price at time of purchase
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price  # saves current price
            )

            # reduce stock automatically
            product.reduce_stock(quantity)

        # calculate total after all items are created
        order.calculate_total()
        return order