"""
Forms used on admin panel for this app.
"""
from datetime import timedelta

from django import forms
from django.utils import timezone


class WarehouseTransactionForm(forms.Form):
    """
    Form for generating warehouse transactions report.
    """

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    start_date = forms.DateField(
        initial=timezone.now().date() - timedelta(weeks=4),
        label="Start Date",
        widget=forms.DateInput(attrs={"type": "date", "format": "%d/%m/%Y"}),
        input_formats=["%d/%m/%Y"],
    )
    end_date = forms.DateField(
        initial=timezone.now().date(),
        label="End Date",
        widget=forms.DateInput(attrs={"type": "date", "format": "%d/%m/%Y"}),
        input_formats=["%d/%m/%Y"],
    )
    file_type = forms.ChoiceField(choices=(("xml", "XML"), ("csv", "CSV"), ("xls", "Excel")))
    # bot = forms.ModelChoiceField(Warehouse.objects)
