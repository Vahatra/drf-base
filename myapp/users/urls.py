from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import UserViewSet

app_name = "users"

router = SimpleRouter()
if settings.DEBUG:
    router = DefaultRouter()

router.register("users", UserViewSet, basename="users")
urlpatterns = router.urls
