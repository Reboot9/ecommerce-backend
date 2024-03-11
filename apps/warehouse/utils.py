"""
Module with utility functions.
"""
import xml.etree.ElementTree as ET

from django.http import HttpResponse

from apps.warehouse.resources import TransactionResource


def generate_xml_transactions(transactions) -> str:
    """
    Generate XML string from a list of transactions.
    """
    root = ET.Element("transactions")
    for transaction in transactions:
        transaction_element = ET.SubElement(root, "transaction")
        ET.SubElement(transaction_element, "id").text = str(transaction.id)
        ET.SubElement(transaction_element, "product_name").text = str(transaction.product.name)
        ET.SubElement(transaction_element, "product_code").text = str(
            transaction.product.product_code
        )
        ET.SubElement(transaction_element, "transaction_type").text = str(
            transaction.transaction_type
        )
        ET.SubElement(transaction_element, "quantity").text = str(transaction.quantity)
        ET.SubElement(transaction_element, "consignment_note_number").text = str(
            transaction.consignment_note.number
        )
        ET.SubElement(transaction_element, "consignment_note_date").text = str(
            transaction.consignment_note.consignment_date.strftime("%d.%m.%Y")
        )
        ET.SubElement(transaction_element, "comment").text = str(transaction.comment)
        ET.SubElement(transaction_element, "created").text = str(
            transaction.created_at.strftime("%d.%m.%Y")
        )

    xml_string = ET.tostring(root, encoding="utf-8", method="xml")
    return xml_string


def generate_report(transactions, file_type, start_date, end_date):
    """
    Generate report based on transactions, file type, and date range.

    :param transactions: Queryset of transactions to include in the report.
    :param file_type: Type of file to export (e.g., 'xml', 'csv').
    :param start_date: Start date of the report.
    :param end_date: End date of the report.
    :return: HTTP response with generated report.
    """
    if file_type == "xml":
        # Custom logic for XML filetype
        xml_string = generate_xml_transactions(transactions)
        response = HttpResponse(xml_string, content_type="application/xml")
    else:
        # Export dataset to specified file format
        resource = TransactionResource()
        dataset = resource.export(transactions)
        response = HttpResponse(dataset.export(file_type), content_type=f"application/{file_type}")

    formatted_start_date = start_date.strftime("%d.%m.%Y")
    formatted_end_date = end_date.strftime("%d.%m.%Y")
    response["Content-Disposition"] = (
        f'attachment; filename="transactions_report_'
        f'{formatted_start_date}-{formatted_end_date}.{file_type}"'
    )
    return response
