"""
Module with utility functions.
"""
import xml.etree.ElementTree as ET


def generate_xml(transactions) -> str:
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
