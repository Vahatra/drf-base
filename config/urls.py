from django.conf import settings
from django.urls import include, path

urlpatterns = [
    # Auth
    path("", include("myapp.auth.urls")),
    # User
    path("", include("myapp.users.urls")),
    # Health
    path("", include("myapp.core.urls")),
]

# Django Adomin and API documentation are only available in "local" environment.
if settings.DEBUG and "django.contrib.admin" in settings.INSTALLED_APPS:
    from django.contrib import admin

    urlpatterns += [
        # Django Admin
        path("admin/", admin.site.urls),
    ]

if settings.DEBUG and "drf_spectacular" in settings.INSTALLED_APPS:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        # DRF auth token
        path("schema/", SpectacularAPIView.as_view(), name="api-schema"),  # type: ignore
        path(
            "docs/",
            SpectacularSwaggerView.as_view(url_name="api-schema"),  # type: ignore
            name="api-docs",
        ),
    ]
