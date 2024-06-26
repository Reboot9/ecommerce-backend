"""
URL configuration for ecommerce_backend project.

The `urlpatterns` list routes URLs to views. For more information, please see:
https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples:
- Function views:
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
- Class-based views:
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
- Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

from apps.accounts import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # app endpoints
    path("api/", include("apps.accounts.urls", namespace="accounts")),
    path("api/shop/", include("apps.product.urls", namespace="product")),
    path("api/", include("apps.order.urls", namespace="order")),
    path("api/", include("apps.cart.urls", namespace="cart")),
    # JWT token endpoints
    path("api/token/", views.DecoratedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", views.DecoratedTokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    # Serve static and media files during development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    # Include debug toolbar URLs
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

    # DRF-YASG endpoints
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    schema_view = get_schema_view(
        openapi.Info(
            title="Pet Shop API",  # TODO: replace with our shop name
            default_version="v1",
            description="API endpoints implemented in the shop",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="test@gmail.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
