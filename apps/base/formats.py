"""
This module includes custom file types for django-import-export library.
"""
import dicttoxml
from import_export.formats.base_formats import TextFormat


class XML(TextFormat):
    """
    Custom import-export filetype for xml files.
    """

    def get_title(self) -> str:
        """
        Returns file title type.
        """
        return "xml"

    def is_binary(self) -> bool:
        """
        Returns if this format is binary.
        """
        return False

    def get_extension(self) -> str:
        """
        Returns extension for this format files.
        """
        return ".xml"

    def get_content_type(self) -> str:
        """
        Returns content type for this format files.
        """
        return "application/xml"

    def can_import(self) -> bool:
        """
        Check if importing is allowed.
        """
        return False

    def can_export(self) -> bool:
        """
        Check if exporting is allowed.
        """
        return True

    def export_data(self, dataset, **kwargs) -> bytes:
        """
        Returns format representation for given dataset.
        """
        kwargs.setdefault("attr_type", False)
        return dicttoxml.dicttoxml(dataset.dict)
