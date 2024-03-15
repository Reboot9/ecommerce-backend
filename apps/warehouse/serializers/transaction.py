"""
Serializers related to Transaction model.
"""
from rest_framework import serializers

from apps.warehouse.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a Transaction model.
    """

    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")

    class Meta:
        model = Transaction
        fields = ["id", "transaction_type", "quantity", "comment", "created_at"]
