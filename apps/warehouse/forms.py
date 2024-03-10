"""
Forms used on admin panel for this app.
"""
from datetime import timedelta

from django import forms
from django.utils import timezone


class FileTypeChoices:
    """A class defining constants for different file types and their choices."""

    XML = "xml"
    CSV = "csv"
    JSON = "json"
    XLS = "xls"
    XLSX = "xlsx"

    CHOICES = [
        (XML, "XML"),
        (CSV, "CSV"),
        (JSON, "JSON"),
        (XLS, "XLS"),
        (XLSX, "XLSX"),
    ]


class WarehouseTransactionForm(forms.Form):
    """
    Form for generating warehouse transactions report.
    """

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    start_date = forms.DateField(
        initial=lambda: (timezone.now().date() - timedelta(weeks=4)).strftime("%d/%m/%Y"),
        label="Start Date",
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    end_date = forms.DateField(
        initial=lambda: timezone.now().date().strftime("%d/%m/%Y"),
        label="End Date",
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(attrs={"class": "datepicker"}),
    )
    file_type = forms.ChoiceField(choices=FileTypeChoices.CHOICES)
