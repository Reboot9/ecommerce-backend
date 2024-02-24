"""
Custom forms for admin-related functionality for warehouse app.
"""
from django.core.exceptions import ValidationError
from apps.warehouse.models.warehouse_item import WarehouseItem
from django import forms


class WarehouseItemForm(forms.ModelForm):
    """
    Form for validating WarehouseItem data in the admin.
    """

    class Meta:
        model = WarehouseItem
        fields = "__all__"

    def clean(self):
        """
        Custom clean method to validate WarehouseItem data.
        """
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        if quantity is not None and quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return cleaned_data
