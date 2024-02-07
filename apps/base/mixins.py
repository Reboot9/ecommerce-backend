"""
This file contains mixins for caching.
"""
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.response import Response

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class CachedListView:
    """
    A mixin providing common functionality for retrieving a paginated list.

    Note, that you need to declare get_cache_key method inside your class
    """

    def get_cache_key(self) -> str:
        """
        Method to get the cache key.

        :return: cache key
        """
        raise NotImplementedError(
            f"The 'get_cache_key' method must be implemented in {self.__class__.__name__} class."
        )

    def list(self, request, *args, **kwargs) -> Response:
        """
        Retrieve a paginated list.

        :param request: The HTTP request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: paginated list of data.
        """
        cache_key = self.get_cache_key()

        # Try to get data from cache
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        # If not in cache, fetch from the database
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        # Set data in cache for future requests
        cache.set(cache_key, data, timeout=CACHE_TTL)

        return Response(data)
