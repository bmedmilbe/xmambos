# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from teladoshi.views import (
    ExpeditionViewSet,
    FleetViewSet,
    PlaceViewSet,
    PostsViewSet,
    RestaurantViewSet,
    SouvenirViewSet,
    StayViewSet,
    StopoverViewSet,
)

router = DefaultRouter()
router.register(r"expeditions", ExpeditionViewSet, basename="expeditions")
router.register(r"stays", StayViewSet, basename="stays")
router.register(r"fleets", FleetViewSet, basename="fleets")
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"places", PlaceViewSet, basename="places")
router.register(r"stopovers", StopoverViewSet, basename="stopovers")
router.register(r"souvenirs", SouvenirViewSet, basename="souvenirs")
router.register(r"posts", PostsViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]
