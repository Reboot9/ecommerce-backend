"""
Swagger Schemas for API Documentation.

This module defines reusable Swagger schemas for documenting API endpoints.
These schemas can be imported and used in various views to ensure consistency
and clarity in the API documentation.
"""
from drf_yasg import openapi

access_token_schema = openapi.Schema(
    type=openapi.TYPE_STRING, description="Access token for authenticating API requests."
)

refresh_token_schema = openapi.Schema(
    type=openapi.TYPE_STRING, description="Refresh token for obtaining new access tokens."
)

email_schema = openapi.Schema(
    title="Email",
    type=openapi.TYPE_STRING,
    format="email",
    pattern=r"(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})",
    max_length=255,
)

created_at_schema = openapi.Schema(
    title="Created at", type=openapi.TYPE_STRING, format="date-time"
)

updated_at_schema = openapi.Schema(
    title="Updated at", type=openapi.TYPE_STRING, format="date-time"
)

password_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    format="password",
    min_length=8,
    max_length=128,
    description="User's password.",
)

detail_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"detail": openapi.Schema(title="Response details.", type=openapi.TYPE_STRING)},
)

user_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_NUMBER, description="Unique user identifier."),
        "email": email_schema,
        "createdAt": created_at_schema,
        "updatedAt": updated_at_schema,
        # Add other properties as needed
    },
)
