from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import HealthViewSet

router = SimpleRouter()
if settings.DEBUG:
    router = DefaultRouter()

router.register("health", HealthViewSet, basename="Health")
urlpatterns = router.urls
