from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from .filters import CMSPostShadowFilter, ExpeditionFilter, StayFilter
from .models import (
    Post,
    Expedition,
    Fleet,
    Place,
    Restaurant,
    Souvenir,
    Stay,
    Stopover,
)
from .serializers import (
    ExpeditionSerializer,
    FleetSerializer,
    PlaceSerializer,
    PostSerializer,
    RestaurantSerializer,
    SouvenirSerializer,
    StaySerializer,
    StopoverSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6              # Returns exactly 6 premium guides per click
    page_size_query_param = 'page_size'
    max_page_size = 100





class ExpeditionViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles 'In the Field' logic for specialized guided excursions."""

    queryset = Expedition.objects.filter(is_active=True)
    serializer_class = ExpeditionSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "badge_tags"]
    filterset_class = ExpeditionFilter
    pagination_class = StandardResultsSetPagination


class StayViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles 'Eco Sanctuaries' lodging and villa listings."""

    queryset = Stay.objects.filter(is_active=True)
    serializer_class = StaySerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "location_detail"]
    filterset_class = StayFilter
    pagination_class = StandardResultsSetPagination





class FleetViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles transport assets and rental specifications."""

    queryset = Fleet.objects.filter(is_active=True)
    serializer_class = FleetSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "vehicle_type", "features"]
    pagination_class = StandardResultsSetPagination


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles dining and culinary experience locations."""

    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "subtitle", "location"]


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles points of interest, landmarks, and geographic discovery locations."""

    queryset = Place.objects.filter(is_active=True)
    serializer_class = PlaceSerializer
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["access_type"]
    search_fields = ["name", "description", "access_type"]


class StopoverViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles transit hubs, group transfers, and layover packages."""

    queryset = Stopover.objects.filter(is_active=True)
    serializer_class = StopoverSerializer
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["arrival_city"]
    search_fields = ["name", "description", "arrival_city", "transfer_details"]

class SouvenirViewSet(viewsets.ReadOnlyModelViewSet):
    """Handles local gifts, crafts, and premium product retail items."""

    # Fetch only active items and prefetch generic
    # relation fields to optimize SQL queries
    queryset = Souvenir.objects.filter(is_active=True).prefetch_related('gallery')
    serializer_class = SouvenirSerializer
    lookup_field = "slug"

    # Enable filtering by exact category and full-text searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category"]
    search_fields = ["name", "description"]

class PostsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Queries tenant-isolated rows natively from the shared PostgreSQL schema.
    Utilizes standard DRF search backends out-of-the-box.
    """
    # Note: Using your cms model field 'active' instead of 'is_active'
    queryset = Post.objects.filter(active=True).order_by('-date')
    serializer_class = PostSerializer
    lookup_field = "slug"

    # Fully supported filtering and text search parameters
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['featured']
    search_fields = ['title', 'description', 'text']
    pagination_class = StandardResultsSetPagination
    filterset_class = CMSPostShadowFilter

