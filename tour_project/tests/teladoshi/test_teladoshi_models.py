import pytest
from django.contrib.contenttypes.models import ContentType

from teladoshi.models import (
    Expedition,
    Fleet,
    Place,
    Restaurant,
    ServiceImage,
    Stay,
    Stopover,
    Vendor,
)


@pytest.mark.django_db
def test_vendor(client, new_vendor):
    assert Vendor.objects.count() == 0

    vendor = new_vendor(
        company_name="Wanderlust Adventures Inc.",
        is_verified=True,
        contact_email="operations@wanderlust.com",
        contact_phone="+1-888-555-0123",
        logo="vendors/wanderlust-logo.jpg",
    )
    vendor.save()

    assert Vendor.objects.count() == 1

    assert vendor.id is not None
    assert vendor.company_name == "Wanderlust Adventures Inc."
    assert vendor.is_verified
    assert vendor.contact_email == "operations@wanderlust.com"
    assert vendor.contact_phone == "+1-888-555-0123"
    assert vendor.logo == "vendors/wanderlust-logo.jpg"
    assert str(vendor) == "Wanderlust Adventures Inc."


@pytest.mark.django_db
def test_expedition(client, new_expedition):
    assert Expedition.objects.count() == 0

    expedition = new_expedition(
        name="Jungle Canopy Expedition",
        description="Immersive guided expedition through pristine Amazon "
        "rainforest with expert naturalists and wildlife photographers",
        price=299.99,
        image="services/covers/jungle_canopy_2026_06.jpg",
        is_active=True,
        specialization="Amazon Rainforest Wildlife",
        badge_tags="Wildlife, Photography, Conservation, Adventure, Eco-Tourism",
        mastery_text="Lead by certified naturalists with 15+ years of "
        "Amazon exploration "
        "experience and conservation credentials",
    )
    expedition.save()

    assert Expedition.objects.count() == 1

    assert expedition.id is not None
    assert expedition.name == "Jungle Canopy Expedition"
    assert (
        expedition.description == "Immersive guided expedition through "
        "pristine Amazon rainforest with expert naturalists and "
        "wildlife photographers"
    )
    assert expedition.price == 299.99
    assert expedition.image == "services/covers/jungle_canopy_2026_06.jpg"
    assert expedition.is_active
    assert expedition.specialization == "Amazon Rainforest Wildlife"
    assert (
        expedition.badge_tags
        == "Wildlife, Photography, Conservation, Adventure, Eco-Tourism"
    )
    assert (
        expedition.mastery_text
        == "Lead by certified naturalists with 15+ years of Amazon "
        "exploration experience "
        "and conservation credentials"
    )
    assert str(expedition) == "Jungle Canopy Expedition"


@pytest.mark.django_db
def test_stay(client, new_stay):
    assert Stay.objects.count() == 0

    stay = new_stay(
        name="Eco Lodge",
        description="A beautiful eco-friendly lodge",
        price=129.99,
        image="stay.jpg",
        is_active=True,
        category="Luxury Villa",
        location_detail="Amazon Rainforest",
        amenities="Swimming Pool, WiFi, Restaurant",
    )
    stay.save()

    assert Stay.objects.count() == 1

    assert stay.id is not None
    assert stay.name == "Eco Lodge"
    assert stay.description == "A beautiful eco-friendly lodge"
    assert stay.price == 129.99
    assert stay.image == "stay.jpg"
    assert stay.is_active
    assert stay.category == "Luxury Villa"
    assert stay.location_detail == "Amazon Rainforest"
    assert stay.amenities == "Swimming Pool, WiFi, Restaurant"
    assert str(stay) == "Eco Lodge"


@pytest.mark.django_db
def test_fleet(client, new_fleet):
    assert Fleet.objects.count() == 0

    fleet = new_fleet(
        name="Land Rover",
        description="Rugged 4x4 adventure vehicle",
        price=99.99,
        image="fleet.jpg",
        is_active=True,
        vehicle_type="SUV",
        transmission="Automatic",
        engine="V6 Diesel",
        features="4WD, GPS, Roof Rack",
    )
    fleet.save()

    assert Fleet.objects.count() == 1

    assert fleet.id is not None
    assert fleet.name == "Land Rover"
    assert fleet.description == "Rugged 4x4 adventure vehicle"
    assert fleet.price == 99.99
    assert fleet.image == "fleet.jpg"
    assert fleet.is_active
    assert fleet.vehicle_type == "SUV"
    assert fleet.transmission == "Automatic"
    assert fleet.engine == "V6 Diesel"
    assert fleet.features == "4WD, GPS, Roof Rack"
    assert str(fleet) == "Land Rover"


@pytest.mark.django_db
def test_restaurant(client, new_restaurant):
    assert Restaurant.objects.count() == 0

    restaurant = new_restaurant(
        name="Safari Bistro",
        description="Fine dining in the wild",
        price=59.99,
        image="restaurant.jpg",
        is_active=True,
        subtitle="Culinary Excellence",
        location="Central Park",
        opening_hours="09:00-22:00",
    )
    restaurant.save()

    assert Restaurant.objects.count() == 1

    assert restaurant.id is not None
    assert restaurant.name == "Safari Bistro"
    assert restaurant.description == "Fine dining in the wild"
    assert restaurant.price == 59.99
    assert restaurant.image == "restaurant.jpg"
    assert restaurant.is_active
    assert restaurant.subtitle == "Culinary Excellence"
    assert restaurant.location == "Central Park"
    assert restaurant.opening_hours == "09:00-22:00"
    assert str(restaurant) == "Safari Bistro"


@pytest.mark.django_db
def test_place(client, new_place):
    assert Place.objects.count() == 0

    place = new_place(
        name="Niagara Falls",
        description="Spectacular waterfall destination",
        price=0.00,
        image="place.jpg",
        is_active=True,
        access_type="Free Access",
        coordinates="43.0896,-79.0849",
    )
    place.save()

    assert Place.objects.count() == 1

    assert place.id is not None
    assert place.name == "Niagara Falls"
    assert place.description == "Spectacular waterfall destination"
    assert place.price == 0.00
    assert place.image == "place.jpg"
    assert place.is_active
    assert place.access_type == "Free Access"
    assert place.coordinates == "43.0896,-79.0849"
    assert str(place) == "Niagara Falls"


@pytest.mark.django_db
def test_stopover(client, new_stopover):
    assert Stopover.objects.count() == 0

    stopover = new_stopover(
        name="Lisbon Rest Stop",
        description="Comfortable rest and transfer point",
        price=25.00,
        image="stopover.jpg",
        is_active=True,
        arrival_city="Lisbon",
        pricing_guide_json={"single": 25.00, "couple": 40.00, "group": 100.00},
        transfer_details="Airport to city center transfer included",
    )
    stopover.save()

    assert Stopover.objects.count() == 1

    assert stopover.id is not None
    assert stopover.name == "Lisbon Rest Stop"
    assert stopover.description == "Comfortable rest and transfer point"
    assert stopover.price == 25.00
    assert stopover.image == "stopover.jpg"
    assert stopover.is_active
    assert stopover.arrival_city == "Lisbon"
    assert stopover.pricing_guide_json == {
        "single": 25.00,
        "couple": 40.00,
        "group": 100.00,
    }
    assert stopover.transfer_details == "Airport to city center transfer included"
    assert str(stopover) == "Lisbon Rest Stop"


@pytest.mark.django_db
def test_service_image(client, new_service_image):
    assert ServiceImage.objects.count() == 0

    service_image = new_service_image(
        image="services/gallery/2026/06/jungle_gallery.jpg",
        alt_text="Scenic canopy view of Amazon rainforest",
    )
    service_image.save()

    assert ServiceImage.objects.count() == 1

    assert service_image.id is not None
    assert service_image.image == "services/gallery/2026/06/jungle_gallery.jpg"
    assert service_image.alt_text == "Scenic canopy view of Amazon rainforest"
    assert service_image.content_object is not None
    assert service_image.content_type == ContentType.objects.get_for_model(Expedition)
    assert isinstance(service_image.content_object, Expedition)
    assert str(service_image) == f"Gallery Image {service_image.id} (expedition)"
