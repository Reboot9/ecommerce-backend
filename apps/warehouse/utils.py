"""
Module with utility functions for warehouse app.
"""
from collections import Counter


def calculate_total_quantity(warehouse_serializer_data: list[dict], transaction_type: str) -> int:
    """
    Calculate the total quantity for a specific transaction type across all warehouse data.

    :param warehouse_serializer_data: The serialized warehouse data.
    :param transaction_type: The type of transaction to calculate the total quantity for.
    :return: The total quantity for the specified transaction type.
    """
    quantities = [
        transaction.get("quantity", 0)
        for warehouse_data in warehouse_serializer_data
        for transaction in warehouse_data.get("transactions", [])
        if transaction.get("transaction_type") == transaction_type
    ]
    return sum(quantities)


def calculate_total_quantities(
    warehouse_serializer_data: list[dict], transaction_types: list[str]
) -> Counter:
    """
    Calculate the total quantities for multiple transaction types across all warehouse data.

    :param warehouse_serializer_data: The serialized warehouse data.
    :param transaction_types: The list of transaction types to calculate total quantities for.

    :return: A Counter object containing the total quantities for each transaction type.
    """
    quantities = Counter()
    for transaction_type in transaction_types:
        quantities[transaction_type] = calculate_total_quantity(
            warehouse_serializer_data, transaction_type
        )
    return quantities
