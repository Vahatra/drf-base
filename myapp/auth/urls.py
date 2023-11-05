from django.urls import path
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh,
    token_verify,
)

app_name = "users"

urlpatterns = [
    path("jwt/create/", token_obtain_pair, name="jwt-create"),
    path("jwt/refresh/", token_refresh, name="jwt-refresh"),
    path("jwt/verify/", token_verify, name="jwt-verify"),
]
