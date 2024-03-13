"""
Module for defining resources for django-import-export library.
"""

# class TransactionResource(resources.ModelResource):
#     """
#     Resource class for Transaction model.
#     """
#
#     consignment_note_number = fields.Field(
#         attribute="consignment_note__number",
#         column_name="consignment note number",
#     )
#     consignment_note_date = fields.Field(
#         attribute="consignment_note__consignment_date",
#         column_name="consignment note date",
#         widget=widgets.DateWidget(format="%d.%m.%Y"),
#     )
#     product_name = fields.Field(
#         attribute="product__name",
#         column_name="product",
#     )
#     product_code = fields.Field(
#         attribute="product__product_code",
#         column_name="product code",
#     )
#     transaction_type = fields.Field(
#         attribute="transaction_type",
#         column_name="transaction type",
#     )
#     created_at = fields.Field(
#         attribute="created_at",
#         column_name="created",
#         widget=widgets.DateTimeWidget(format="%d.%m.%Y %H:%M:%S"),
#     )
#
#     class Meta:
#         model = Transaction
#         fields = [
#             "id",
#             "product_name",
#             "product_code",
#             "consignment_note_number",
#             "consignment_note_date",
#             "transaction_type",
#             "quantity",
#             "comment",
#             "created_at",
#         ]
#         export_order = [
#             "id",
#             "product_name",
#             "product_code",
#             "transaction_type",
#             "quantity",
#             "consignment_note_number",
#             "consignment_note_date",
#             "comment",
#             "created_at",
#         ]
#
#
# class WarehouseResource(resources.ModelResource):
#     transactions = fields.Field(column_name="transactions", attribute="transactions",
#                                 widget=TransactionResource())
#
#     product_name = fields.Field(
#         attribute="product__name",
#         column_name="product",
#     )
#     product_code = fields.Field(
#         attribute="product__product_code",
#         column_name="product code",
#     )
#
#     class Meta:
#         model = Warehouse
#         fields = [
#             "id",
#             "product_name",
#             "total_balance",
#             "product_code",
#             "transactions",
#         ]
#         export_order = [
#             "id",
#             "product_name",
#             "total_balance",
#             "product_code",
#             "transactions",
#         ]
