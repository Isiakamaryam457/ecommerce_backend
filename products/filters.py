import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # filter by category name
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    
    # filter by price range
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # filter by stock availability
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0)  # stock greater than 0
        return queryset.filter(stock_quantity=0)  # out of stock

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'in_stock']