"""
Module: views.py.

This module contains handler for the manufacturer.
"""
from rest_framework.generics import ListAPIView

from apps.product.models import Manufacturer
from apps.product.serializers.manufacturer import ManufacturerSerializer


class ManufacturerListView(ListAPIView):
    """Returns a list of manufacturer."""

    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()
