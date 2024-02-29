"""
This model is used to record consignment notes in the GoodsArrival and GoodsConsumption models.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseID, BaseDate


class ConsignmentNote(BaseID, BaseDate):
    """
    Represents a consignment note with a unique number and sign date.
    """

    number = models.CharField(
        max_length=250,
        unique=True,
        help_text=_(
            "Consignment note number. "
            "Note that this field accepts letters and other characters."
        ),
    )
    consignment_date = models.DateField(help_text=_("The date of the consignment note document."))

    class Meta:
        ordering = ["-created_at"]
        db_table = "consignment_note"
        verbose_name = _("Consignment Note")
        verbose_name_plural = _("Consignment Notes")
        unique_together = ["number", "consignment_date"]
        indexes = [
            models.Index(fields=["consignment_date"], name="idx_consignment_note_date"),
        ]

    def __str__(self):
        """
        Returns a string representation of the consignment note.

        :return: string representation of model
        """
        return f"Consignment Note #{self.number} - {self.consignment_date.strftime('%d.%m.%Y')}"
