"""
Validators that can be used in all project.
"""
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


# Define the regular expression pattern to exclude special characters
special_characters_pattern = r"^[a-zA-Z0-9]+$"

# Create a validator using the RegexValidator
special_characters_validator = RegexValidator(
    regex=special_characters_pattern,
    message=_("Special characters are not allowed."),
    code="invalid_special_characters",
)
