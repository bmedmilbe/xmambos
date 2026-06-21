
import pytest # noqa: I001
from core.models import Domain
from django_tenants.utils import get_tenant_model
from rest_framework import status
from rest_framework.test import APIClient

from teladoshi.models import (
    Expedition,
    Fleet,
    Place,
    Restaurant,
    Stay,
    Stopover,
)


@pytest.fixture
def tenant_client(db):
    """
    Creates an APIClient pre-configured to match test_order_views host configurations.
    """
    client = APIClient()
    client.credentials(
        HTTP_HOST="test.localhost",
        SERVER_NAME="test.localhost",
        HTTP_X_TENANT="test",
        X_TENANT="test"
    )
    return client


@pytest.fixture
def setup_tenant_domain():
    """
    Ensures the domain configuration maps correctly to resolve 404 routing errors.
    """

    TenantModel = get_tenant_model()
    test_tenant = TenantModel.objects.get(schema_name="test")
    Domain.objects.get_or_create(domain="test.teladoshi.com",
                                 tenant=test_tenant, is_primary=False)


# --- EXPEDITION VIEWSET TESTS ---

@pytest.mark.django_db
def test_expedition_list_and_detail(tenant_client, setup_tenant_domain, new_vendor):
    vendor = new_vendor()
    vendor.save()

    active_expedition = Expedition.objects.create(
        name="Amazon Jungle Guided Trek",
        slug="amazon-jungle-trek",
        price=350.00,
        is_active=True,
        specialization="Rainforest Navigation",
        badge_tags="Adventure, Wildlife",
        mastery_text="Expert guides with over 10 years of pathfinding experience.",
        vendor=vendor
    )

    # Test List Query (Only returns active items)
    url = "/api/expeditions/"
    response = tenant_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]["slug"] == "amazon-jungle-trek"

    # Test Search Filters
    response = tenant_client.get(f"{url}?search=Jungle")
    assert "results" in response.data
    assert len(response.data['results']) == 1

    # Test Detail Lookup by Slug
    detail_url = f"/api/expeditions/{active_expedition.slug}/"
    response = tenant_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Amazon Jungle Guided Trek"


# --- STAY VIEWSET TESTS ---

@pytest.mark.django_db
def test_stay_list_and_search(tenant_client, setup_tenant_domain, new_vendor):
    vendor = new_vendor()
    vendor.save()

    Stay.objects.create(
        name="Eco Canopy Treehouse Villa",
        slug="eco-canopy-treehouse",
        price=180.00,
        is_active=True,
        category="Sanctuary Lodging",
        location_detail="Costa Rica Rainforest Canopy Sector 4",
        amenities="Solar Energy, Rainwater Collection",
        vendor=vendor
    )

    url = "/api/stays/"
    response = tenant_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data['results']) == 1

    response = tenant_client.get(f"{url}?search=Treehouse")
    assert "results" in response.data
    assert len(response.data['results']) == 1


# --- FLEET VIEWSET TESTS ---

@pytest.mark.django_db
def test_fleet_list_and_filters(tenant_client, setup_tenant_domain, new_vendor):
    vendor = new_vendor()
    vendor.save()

    Fleet.objects.create(
        name="Overland Safari 4x4 Cruiser",
        slug="overland-safari-4x4",
        price=120.00,
        is_active=True,
        vehicle_type="SUV Camper Truck",
        transmission="Manual",
        engine="3.0L Turbo Diesel",
        features="Roof Tent, Recovery Winch, Fridge",
        vendor=vendor
    )

    url = "/api/fleet/"
    response = tenant_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data['results']) == 1

    response = tenant_client.get(f"{url}?search=Winch")
    assert "results" in response.data
    assert len(response.data['results']) == 1


# --- RESTAURANT VIEWSET TESTS ---

@pytest.mark.django_db
def test_restaurant_list_and_detail(tenant_client, setup_tenant_domain, new_vendor):
    vendor = new_vendor()
    vendor.save()

    restaurant = Restaurant.objects.create(
        name="The Organic Forager Kitchen",
        slug="organic-forager-kitchen",
        price=45.00,
        is_active=True,
        subtitle="Farm-to-Table Gastronomy",
        location="Highlands Valley Road Mile 12",
        opening_hours="12:00 - 22:00",
        vendor=vendor
    )

    url = "/api/restaurants/"
    response = tenant_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data['results']) == 1

    detail_url = f"/api/restaurants/{restaurant.slug}/"
    response = tenant_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK


# --- PLACE VIEWSET TESTS ---

@pytest.mark.django_db
def test_place_list_and_filterset(tenant_client, setup_tenant_domain, new_vendor):
    vendor = new_vendor()
    vendor.save()

    Place.objects.create(
        name="Ancient Caldera Overlook Point",
        slug="ancient-caldera-overlook",
        price=0.00,
        is_active=True,
        access_type="Public Reservation Required",
        coordinates="10.2345 N, -84.1234 W",
        vendor=vendor
    )

    url = "/api/places/"
    response = tenant_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data['results']) == 1

    response = tenant_client.get(f"{url}?access_type=Public Reservation Required")
    assert "results" in response.data
    assert len(response.data['results']) == 1


# --- STOPOVER VIEWSET TESTS ---

@pytest.mark.django_db
def test_stopover_list_and_search_logic(tenant_client, setup_tenant_domain, new_vendor):
    vendor = new_vendor()
    vendor.save()

    Stopover.objects.create(
        name="San José Airport VIP Direct Transfer Package",
        slug="sjo-airport-vip-transfer",
        price=75.00,
        is_active=True,
        arrival_city="San José",
        pricing_guide_json='{"base": 75, "extra_luggage": 15}',
        transfer_details="Private air-conditioned shuttle with bilingual escort agent.",
        vendor=vendor
    )

    url = "/api/stopovers/"
    response = tenant_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data['results']) == 1

    response = tenant_client.get(f"{url}?arrival_city=San José")
    assert "results" in response.data
    assert len(response.data['results']) == 1
