"""
Serializers related to Warehouse model.
"""
from datetime import timedelta
from typing import List

from rest_framework import serializers

from apps.warehouse.models import Warehouse
from apps.warehouse.serializers.transaction import TransactionSerializer


class WarehouseSerializer(serializers.ModelSerializer):
    """
    Serializer for warehouse items with their transactions.
    """

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.product_code", read_only=True)
    transactions = (
        serializers.SerializerMethodField()
    )  # TransactionSerializer(many=True, read_only=True)
    sold_items = serializers.SerializerMethodField()
    written_off_items = serializers.SerializerMethodField()
    returned_items = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = [
            "id",
            "product_name",
            "product_code",
            "total_balance",
            "sold_items",
            "written_off_items",
            "returned_items",
            "transactions",
        ]

    def get_transactions(self, obj) -> List[dict]:
        """
        Retrieve transactions related to the warehouse within a specified date range.

        :param obj: warehouse instance
        :return: serialized data of transactions
        """
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")
        if start_date and end_date:
            transactions = obj.product.transactions.filter(
                created_at__range=(start_date, end_date + timedelta(days=1)), is_active=True
            )
        else:
            transactions = obj.product.transactions.filter(is_active=True)

        return TransactionSerializer(transactions, many=True).data

    def get_items_count(self, obj, transaction_type: str) -> int:
        """
        Helper method to count items of specific transaction type.
        """
        transactions = self.get_transactions(obj)
        return sum(
            transaction.get("quantity", 0)
            for transaction in transactions
            if transaction.get("transaction_type") == transaction_type
        )

    def get_sold_items(self, obj) -> int:
        """
        Retrieves quantity of ordered items for the warehouse.

        :param obj: warehouse instance
        :return: total quantity of sold items
        """
        return self.get_items_count(obj, "order")

    def get_written_off_items(self, obj) -> int:
        """
        Retrieves quantity of written off items for the warehouse.

        :param obj: warehouse instance
        :return: total quantity of written off items
        """
        return self.get_items_count(obj, "write_off")

    def get_returned_items(self, obj) -> int:
        """
        Retrieves quantity of returned items for the warehouse.

        :param obj: warehouse instance
        :return: total quantity of returned items
        """
        return self.get_items_count(obj, "return")
