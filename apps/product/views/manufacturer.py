"""
This module contains manufacturer-related views.
"""
from rest_framework.generics import ListAPIView

from apps.product.models import Manufacturer
from apps.product.serializers.manufacturer import ManufacturerSerializer


class ManufacturerListView(ListAPIView):
    """
    API endpoint that returns a list of manufacturers.
    """

    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()
