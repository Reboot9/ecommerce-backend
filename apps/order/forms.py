"""
Module: forms.py.

Contains custom forms for managing Delivery model in Django admin.
"""
from django import forms

from apps.order.models.delivery import Delivery


class DeliveryModelAdminForm(forms.ModelForm):
    """A custom form for managing Delivery model in Django admin."""

    class Meta:
        model = Delivery
        fields = (
            "option",
            "city",
            "street",
            "house",
            "flat",
            "floor",
            "entrance",
            "time",
            "department",
            "declaration",
        )

    def clean(self):
        """Clean method to validate fields based on the value of the 'option' field."""
        cleaned_data = super().clean()

        if cleaned_data.get("option") == "C":
            for field in ("street", "house", "entrance", "time"):
                if not cleaned_data.get(field):
                    self.add_error(field, "This field is required")
        elif cleaned_data.get("option") == "D":
            if not cleaned_data.get("department"):
                self.add_error("department", "This field is required")
        return cleaned_data
