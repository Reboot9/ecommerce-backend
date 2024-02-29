"""
This model is used to record consignment notes in the GoodsArrival and GoodsConsumption models.
"""
from django.core.exceptions import ValidationError
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
        help_text=_("Consignment note number"),
    )
    consignment_date = models.DateField(help_text=_("The date of the consignment note document."))
    # goods_arrival = models.OneToOneField(
    #     GoodsArrival,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    # goods_consumption = models.OneToOneField(
    #     GoodsConsumption,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )

    class Meta:
        ordering = ["-created_at"]
        db_table = "consignment_note"
        verbose_name = _("Consignment Note")
        verbose_name_plural = _("Consignment Notes")
        unique_together = ["number", "consignment_date"]  # переименовать в дату прихода накладной
        indexes = [
            models.Index(fields=["consignment_date"], name="idx_consignment_note_date"),
        ]

    def __str__(self):
        """
        Returns a string representation of the consignment note.

        :return: string representation of model
        """
        return f"{self.number} - {self.sign_date.strftime('%d.%m.%Y')}"

    def clean(self) -> None:
        """
        Modifying clean method to enforce that only one goods operation.
        """
        if self.goods_arrival and self.goods_consumption:
            raise ValidationError(
                _("Only one of goods_arrival or goods_consumption can be filled at once.")
            )
        elif not self.goods_arrival and not self.goods_consumption:
            raise ValidationError(
                _("At least one of goods_arrival or goods_consumption must be filled.")
            )
