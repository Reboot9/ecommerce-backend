"""
Contains custom pagination classes for the app.

These paginators can be used to control the number of items per page,
set query parameters for page size, and enforce maximum page size limits.
"""
from rest_framework.pagination import PageNumberPagination


class CustomUserPagination(PageNumberPagination):
    """
    Custom pagination class for `CustomUser` viewset.

    This pagination class extends the DRF `PageNumberPagination` class
    and sets specific attributes for paginating a list of `CustomUser` instances.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
