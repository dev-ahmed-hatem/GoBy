from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        no_pagination = request.query_params.get('no_pagination')
        if no_pagination:
            return None
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        total_pages = ceil(count / self.page_size)
        message = "Data retrieved successfully" if count > 0 else "No results found"

        return Response({
            "meta": {
                'total_pages': total_pages,
                'current_page': self.page.number,
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'data': data,
            "message": message,
        })
