"""
Common Pagination Module.

This module contains a custom pagination class for lists of instances in
a Django REST framework application.
"""
from rest_framework.pagination import PageNumberPagination


class PaginationCommon(PageNumberPagination):
    """
    This class sets certain attributes for pagination of a list of instances.

    If you need other pagination conditions, create your own class.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
