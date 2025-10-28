from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, EventViewSet

# Описание маршрутизации для ViewSet
router = DefaultRouter()

router.register("event", EventViewSet, basename="event")
router.register("", BookingViewSet, basename="booking")


urlpatterns = router.urls
