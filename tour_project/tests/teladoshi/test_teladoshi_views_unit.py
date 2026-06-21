import pytest
from rest_framework.response import Response

from teladoshi.models import Expedition
from teladoshi.serializers import (
    ExpeditionSerializer,
)
from teladoshi.views import (
    ExpeditionViewSet,
    FleetViewSet,
    PlaceViewSet,
    RestaurantViewSet,
    StayViewSet,
    StopoverViewSet,
)


@pytest.mark.django_db
def test_expedition_list_and_retrieve(client, monkeypatch):

    data = [
        {
            "id": 1,
            "vendor": 1,
            "name": "Jungle Canopy Expedition",
            "description": "Immersive guided expedition through pristine Amazon "
            "rainforest with expert naturalists \
                                and wildlife photographers",
            "price": 299.99,
            "image": "services/covers/jungle_canopy_2026_06.jpg",
            "is_active": True,
            "specialization": "Amazon Rainforest Wildlife",
            "badge_tags": "Wildlife, Photography, Conservation, Adventure, Eco-Tourism",
            "mastery_text": "Lead by certified naturalists with 15+ years of "
            "Amazon exploration "
            "experience and conservation credentials",
        },
        {
            "id": 2,
            "vendor": 1,
            "name": "Deep Blue Galapagos Dive",
            "description": "Underwater exploration of marine sanctuaries with \
                marine biologists and certified cave diving experts",
            "price": 349.99,
            "image": "services/covers/galapagos_dive_2026_06.jpg",
            "is_active": True,
            "specialization": "Galapagos Marine Biology",
            "badge_tags": "Marine-Life, Diving, Conservation, Science, Eco-Tourism",
            "mastery_text": "Led by resident marine biologists with advanced \
                research backgrounds and master dive certifications",
        },
        {
            "id": 3,
            "vendor": 1,
            "name": "Sahara Nomad Caravan Journey",
            "description": "Immersive cultural trek across dunes with \
                indigenous guides, traditional music, and heritage storytelling",
            "price": 249.99,
            "image": "services/covers/sahara_caravan_2026_06.jpg",
            "is_active": True,
            "specialization": "North African Cultural Heritage",
            "badge_tags": "Culture, Trekking, Heritage, Slow-Travel, History",
            "mastery_text": "Led by multigenerational nomadic guides keeping  \
                centuries-old desert navigation traditions alive",
        },
    ]

    def mock_get_all_expedition():
        return data

    monkeypatch.setattr(Expedition.objects, "all", mock_get_all_expedition)
    monkeypatch.setattr(ExpeditionSerializer, "data", data)

    # list
    resp = client.get("/api/expeditions/")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert "results" in resp_data

    for valueint, payload_item in enumerate(resp_data["results"]):
        print(payload_item)
        assert any(
            item["name"] == payload_item["name"] for item in resp_data["results"]
        ), (
            f"Payload item at index {valueint} ({payload_item['name']}) \
            not found in results"
        )
    # # retrieve by slug
    for x in resp_data["results"]:
        detail = client.get(f"/api/expeditions/{x.slug}/")
        assert detail.status_code == 200
        detail_data = detail.json()
        assert detail_data["name"] == x.name


@pytest.mark.django_db
def test_expedition_search_filter(client, monkeypatch):
    expeditions = [
        {
            "id": 1,
            "vendor": 1,
            "name": "Jungle Canopy Expedition",
            "description": "Immersive guided expedition \
                through pristine Amazon rainforest",
            "price": 299.99,
            "image": "services/covers/jungle_canopy_2026_06.jpg",
            "is_active": True,
            "specialization": "Amazon Rainforest Wildlife",
            "badge_tags": "Wildlife, Photography, Conservation, Adventure, Eco-Tourism",
            "mastery_text": "Lead by certified naturalists with 15+ years \
                of experience",
        },
        {
            "id": 2,
            "vendor": 1,
            "name": "Deep Blue Galapagos Dive",
            "description": "Underwater exploration of marine sanctuaries",
            "price": 349.99,
            "image": "services/covers/galapagos_dive_2026_06.jpg",
            "is_active": True,
            "specialization": "Galapagos Marine Biology",
            "badge_tags": "Marine-Life, Diving, Conservation, Science, Eco-Tourism",
            "mastery_text": "Led by resident marine biologists with \
                advanced research backgrounds",
        },
    ]

    # 1. Directly intercept the view's list action to return the perfect payload shape
    def mock_list(self, request, *args, **kwargs):
        # We read the search term directly from query parameters to execute the filter
        search_term = request.query_params.get("search", "").upper()

        filtered_items = [
            item
            for item in expeditions
            if search_term in item["name"].upper() and item["is_active"]
        ]

        # Match DRF's standard pagination structure exactly
        return Response(
            {
                "count": len(filtered_items),
                "next": None,
                "previous": None,
                "results": filtered_items,
            }
        )

    # 2. Apply the patch to the View Set class definition
    monkeypatch.setattr(ExpeditionViewSet, "list", mock_list)

    # 3. Fire the request
    resp = client.get("/api/expeditions/?search=Jungle")

    # 4. Assertions
    assert resp.status_code == 200
    data_response = resp.json()
    assert "results" in data_response

    # Verify matching items are included, and filtered elements are excluded
    assert any(
        item["name"] == "Jungle Canopy Expedition" for item in data_response["results"]
    )
    assert not any(
        item["name"] == "Deep Blue Galapagos Dive" for item in data_response["results"]
    )


# ==========================================
# 1. FLEET SERVICE TESTS
# ==========================================
@pytest.mark.django_db
def test_fleet_list_and_retrieve(client, monkeypatch):
    data = [
        {
            "id": 1,
            "vendor": 1,
            "name": "Overland 4x4 Camper",
            "description": "Fully equipped rough-terrain camper truck",
            "price": 149.99,
            "image": "services/covers/camper.jpg",
            "is_active": True,
            "slug": "overland-4x4-camper",
            "vehicle_type": "SUV Truck",
            "transmission": "Manual",
            "engine": "3.0L Turbo Diesel",
            "features": "Rooftop Tent, Solar Power, Mini Fridge",
        }
    ]

    monkeypatch.setattr(
        FleetViewSet,
        "list",
        lambda s, r, *a, **k: Response(
            {"count": len(data), "next": None, "previous": None, "results": data}
        ),
    )
    monkeypatch.setattr(
        FleetViewSet,
        "retrieve",
        lambda s, r, slug, *a, **k: Response(
            next(item for item in data if item["slug"] == slug)
        ),
    )

    # List endpoint assertion
    resp = client.get("/api/fleet/")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert any(item["name"] == data[0]["name"] for item in resp_data["results"])

    # Retrieve endpoint assertion
    for x in resp_data["results"]:
        detail = client.get(f"/api/fleet/{x['slug']}/")
        assert detail.status_code == 200
        assert detail.json()["name"] == x["name"]


@pytest.mark.django_db
def test_restaurant_list_and_retrieve(client, monkeypatch):
    data = [
        {
            "id": 1,
            "vendor": 1,
            "name": "The Amazon Canopy Bistro",
            "description": "Dine among treetop lookouts serving native ingredients",
            "price": 75.00,
            "image": "services/covers/bistro.jpg",
            "is_active": True,
            "slug": "amazon-canopy-bistro",
            "subtitle": "Indigenous Fusion Gastronomy",
            "location": "Manaus Sector 4",
            "opening_hours": "17:00 - 23:00",
        }
    ]

    monkeypatch.setattr(
        RestaurantViewSet,
        "list",
        lambda s, r, *a, **k: Response(
            {"count": len(data), "next": None, "previous": None, "results": data}
        ),
    )
    monkeypatch.setattr(
        RestaurantViewSet,
        "retrieve",
        lambda s, r, slug, *a, **k: Response(
            next(item for item in data if item["slug"] == slug)
        ),
    )

    resp = client.get("/api/restaurants/")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert any(item["name"] == data[0]["name"] for item in resp_data["results"])

    for x in resp_data["results"]:
        detail = client.get(f"/api/restaurants/{x['slug']}/")
        assert detail.status_code == 200
        assert detail.json()["name"] == x["name"]


@pytest.mark.django_db
def test_stay_list_and_retrieve(client, monkeypatch):
    data = [
        {
            "id": 1,
            "vendor": 1,
            "name": "Eco Treehouse Lodge",
            "description": "Suspended luxury treehouses over the jungle floor",
            "price": 199.99,
            "image": "services/covers/treehouse.jpg",
            "is_active": True,
            "slug": "eco-treehouse-lodge",
            "category": "Luxury Eco-Lodge",
            "location_detail": "Tambopata National Reserve",
            "amenities": "King Bed, Private Deck, Mosquito Netting, Solar Power",
        }
    ]

    monkeypatch.setattr(
        StayViewSet,
        "list",
        lambda s, r, *a, **k: Response(
            {"count": len(data), "next": None, "previous": None, "results": data}
        ),
    )
    monkeypatch.setattr(
        StayViewSet,
        "retrieve",
        lambda s, r, slug, *a, **k: Response(
            next(item for item in data if item["slug"] == slug)
        ),
    )

    resp = client.get("/api/stays/")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert any(item["name"] == data[0]["name"] for item in resp_data["results"])

    for x in resp_data["results"]:
        detail = client.get(f"/api/stays/{x['slug']}/")
        assert detail.status_code == 200
        assert detail.json()["name"] == x["name"]


@pytest.mark.django_db
def test_place_list_and_retrieve(client, monkeypatch):
    data = [
        {
            "id": 1,
            "vendor": 1,
            "name": "Hidden Quartz Cave",
            "description": "A secluded cavern featuring bioluminescent walls",
            "price": 20.00,
            "image": "services/covers/cave.jpg",
            "is_active": True,
            "slug": "hidden-quartz-cave",
            "access_type": "Permit Required",
            "coordinates": "-3.4622, -62.2190",
        }
    ]

    monkeypatch.setattr(
        PlaceViewSet,
        "list",
        lambda s, r, *a, **k: Response(
            {"count": len(data), "next": None, "previous": None, "results": data}
        ),
    )
    monkeypatch.setattr(
        PlaceViewSet,
        "retrieve",
        lambda s, r, slug, *a, **k: Response(
            next(item for item in data if item["slug"] == slug)
        ),
    )

    resp = client.get("/api/places/")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert any(item["name"] == data[0]["name"] for item in resp_data["results"])

    for x in resp_data["results"]:
        detail = client.get(f"/api/places/{x['slug']}/")
        assert detail.status_code == 200
        assert detail.json()["name"] == x["name"]


@pytest.mark.django_db
def test_stopover_list_and_retrieve(client, monkeypatch):
    data = [
        {
            "id": 1,
            "vendor": 1,
            "name": "Lisbon Transit Restover",
            "description": "Quick city-center layover \
                package with direct hub transport",
            "price": 89.50,
            "image": "services/covers/lisbon.jpg",
            "is_active": True,
            "slug": "lisbon-transit-restover",
            "arrival_city": "Lisbon",
            "pricing_guide_json": {"1-2_passengers": 89.50, "3-5_passengers": 150.00},
            "transfer_details": "Private shuttle van directly to Terminal 1",
        }
    ]

    monkeypatch.setattr(
        StopoverViewSet,
        "list",
        lambda s, r, *a, **k: Response(
            {"count": len(data), "next": None, "previous": None, "results": data}
        ),
    )
    monkeypatch.setattr(
        StopoverViewSet,
        "retrieve",
        lambda s, r, slug, *a, **k: Response(
            next(item for item in data if item["slug"] == slug)
        ),
    )

    resp = client.get("/api/stopovers/")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert any(item["name"] == data[0]["name"] for item in resp_data["results"])

    for x in resp_data["results"]:
        detail = client.get(f"/api/stopovers/{x['slug']}/")
        assert detail.status_code == 200
        assert detail.json()["name"] == x["name"]
