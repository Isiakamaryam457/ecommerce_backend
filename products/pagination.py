from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,                          # current page
            'total_pages': self.page.paginator.num_pages,      # total pages
            'total_products': self.page.paginator.count,       # total products
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })