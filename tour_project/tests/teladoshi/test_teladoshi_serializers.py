from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile

from teladoshi.models import ServiceImage
from teladoshi.serializers import (
    CatalogReviewSerializer,
    ExpeditionSerializer,
    FleetSerializer,
    PlaceSerializer,
    RestaurantSerializer,
    ServiceImageSerializer,
    StaySerializer,
    StopoverSerializer,
    VendorSerializer,
)

User = get_user_model()


def test_valid_service_image_serializer(new_expedition):
    expedition = new_expedition()
    expedition.save()

    content_type = ContentType.objects.get_for_model(expedition)
    fake_image = SimpleUploadedFile(
        name="image.jpg",
        content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
        content_type="image/jpeg",
    )

    valid_input_data = {
        "image": fake_image,
        "alt_text": "alt_text",
        "object_id": expedition.id,
        "content_type": content_type.id,
    }

    serializer = ServiceImageSerializer(data=valid_input_data)
    assert serializer.is_valid(), serializer.errors

    saved_instance = serializer.save()

    fresh_db_instance = ServiceImage.objects.get(id=saved_instance.id)

    read_serializer = ServiceImageSerializer(instance=fresh_db_instance)

    assert read_serializer.data["attached_to"]["id"] == expedition.id
    assert read_serializer.data["attached_to"]["model_type"] == "expedition"


def test_valid_catalog_review_serializer(new_expedition):
    expedition = new_expedition()
    expedition.save()

    user = User.objects.create(username="testclient")

    CustomerTargetModel = apps.get_model("order", "Customer")
    customer = CustomerTargetModel.objects.create(user=user)
    content_type = ContentType.objects.get_for_model(expedition)

    valid_input_data = {
        "customer": customer.id,
        "object_id": expedition.id,
        "content_type": content_type.id,
        "content": "Text content",
        "rating": 4,
    }

    serializer = CatalogReviewSerializer(data=valid_input_data)
    assert serializer.is_valid(), serializer.errors

    saved_instance = serializer.save()
    TargetModel = apps.get_model("order", "Review")
    fresh_db_instance = TargetModel.objects.get(id=saved_instance.id)

    read_serializer = CatalogReviewSerializer(instance=fresh_db_instance)

    assert read_serializer.data["attached_to"]["id"] == expedition.id
    assert read_serializer.data["attached_to"]["model_type"] == "expedition"


def test_valid_vendor_serializer():

    valid_input_data = {
        "logo": None,
        "is_verified": True,
        "company_name": "ABC Corp",
        "contact_email": "vendor@example.com",
        "contact_phone": "12345678",
    }

    serializer = VendorSerializer(data=valid_input_data)
    assert serializer.is_valid(), serializer.errors
    serializer.save()
    assert serializer.validated_data["company_name"] == "ABC Corp"
    assert serializer.data["id"]
    # update via serializer
    vendor_id = serializer.data["id"]
    VendorModel = apps.get_model("teladoshi", "Vendor")
    vendor_instance = VendorModel.objects.get(id=vendor_id)
    update_data = {"company_name": "New Name", "contact_email": "new@example.com"}
    update_serializer = VendorSerializer(
        instance=vendor_instance, data=update_data, partial=True
    )
    assert update_serializer.is_valid(), update_serializer.errors
    updated = update_serializer.save()
    assert updated.company_name == "New Name"


def _common_service_checks(serialized, instance):
    # ExpeditionSerializer exposes a nested `vendor` object; others use `vendor_name`
    if "vendor_name" in serialized.data:
        assert serialized.data["vendor_name"] == instance.vendor.company_name
        assert serialized.data["is_vendor_verified"] == instance.vendor.is_verified
    else:
        # nested vendor object
        assert serialized.data["vendor"]["company_name"] == instance.vendor.company_name
        assert serialized.data["vendor"]["is_verified"] == instance.vendor.is_verified
    assert serialized.data["name"] == instance.name
    assert isinstance(serialized.data["gallery"], list)
    assert isinstance(serialized.data["reviews"], list)


def test_expedition_serializer_fields(new_expedition):
    expedition = new_expedition()
    expedition.save()

    # attach a gallery image
    ServiceImage.objects.create(
        image="services/gallery/test.jpg", alt_text="img", content_object=expedition
    )

    serializer = ExpeditionSerializer(instance=expedition)
    _common_service_checks(serializer, expedition)
    assert serializer.data["specialization"] == expedition.specialization


def _make_vendor(new_vendor):
    v = new_vendor()
    v.save()
    return v


def _service_create_and_update_tests(
    serializer_class, model_name, create_kwargs, new_fixture=None
):
    # create
    VendorModel = apps.get_model("teladoshi", "Vendor")
    v = VendorModel.objects.create(
        company_name="Creator",
        contact_email="a@b.com",
        contact_phone="1",
        is_verified=False,
    )
    data = {**create_kwargs, "vendor_id": v.id}
    # provide a fake uploaded file for ImageField
    fake_image = SimpleUploadedFile(
        name="img.jpg",
        content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
        content_type="image/jpeg",
    )
    if "image" in data:
        data["image"] = fake_image
    serializer = serializer_class(data=data)
    assert serializer.is_valid(), serializer.errors
    saved = serializer.save()
    Model = apps.get_model("teladoshi", model_name)
    obj = Model.objects.get(id=saved.id)
    assert obj.name == create_kwargs["name"]

    # update
    upd_serializer = serializer_class(
        instance=obj, data={"name": "Updated Name"}, partial=True
    )
    assert upd_serializer.is_valid(), upd_serializer.errors
    updated = upd_serializer.save()
    assert updated.name == "Updated Name"


def test_create_update_expedition_serializer():
    _service_create_and_update_tests(
        ExpeditionSerializer,
        "Expedition",
        {
            "name": "Create X",
            "description": "desc",
            "price": 10.0,
            "image": "img.jpg",
            "is_active": True,
            "specialization": "spec",
            "badge_tags": "tags",
            "mastery_text": "master",
        },
    )


def test_create_update_stay_serializer():
    _service_create_and_update_tests(
        StaySerializer,
        "Stay",
        {
            "name": "Stay Create",
            "description": "desc",
            "price": 20.0,
            "image": "img.jpg",
            "is_active": True,
            "category": "cat",
            "location_detail": "loc",
            "amenities": "wifi",
        },
    )


def test_create_update_fleet_serializer():
    _service_create_and_update_tests(
        FleetSerializer,
        "Fleet",
        {
            "name": "Fleet Create",
            "description": "desc",
            "price": 30.0,
            "image": "img.jpg",
            "is_active": True,
            "vehicle_type": "SUV",
            "transmission": "Automatic",
            "engine": "V6",
            "features": "4x4",
        },
    )


def test_create_update_restaurant_serializer():
    _service_create_and_update_tests(
        RestaurantSerializer,
        "Restaurant",
        {
            "name": "Rest Create",
            "description": "desc",
            "price": 40.0,
            "image": "img.jpg",
            "is_active": True,
            "subtitle": "sub",
            "location": "loc",
            "opening_hours": "08:00-22:00",
        },
    )


def test_create_update_place_serializer():
    _service_create_and_update_tests(
        PlaceSerializer,
        "Place",
        {
            "name": "Place Create",
            "description": "desc",
            "price": 0.0,
            "image": "img.jpg",
            "is_active": True,
            "access_type": "Free Access",
            "coordinates": "0,0",
        },
    )


def test_create_update_stopover_serializer():
    _service_create_and_update_tests(
        StopoverSerializer,
        "Stopover",
        {
            "name": "Stop Create",
            "description": "desc",
            "price": 5.0,
            "image": "img.jpg",
            "is_active": True,
            "arrival_city": "City",
            "pricing_guide_json": {"single": 5.0},
            "transfer_details": "details",
        },
    )


def test_stay_serializer_fields(new_stay):
    stay = new_stay()
    stay.save()

    ServiceImage.objects.create(
        image="services/gallery/stay.jpg", alt_text="img", content_object=stay
    )

    serializer = StaySerializer(instance=stay)
    _common_service_checks(serializer, stay)
    assert serializer.data["category"] == stay.category


def test_fleet_serializer_fields(new_fleet):
    fleet = new_fleet()
    fleet.save()

    ServiceImage.objects.create(
        image="services/gallery/fleet.jpg", alt_text="img", content_object=fleet
    )

    serializer = FleetSerializer(instance=fleet)
    _common_service_checks(serializer, fleet)
    assert serializer.data["vehicle_type"] == fleet.vehicle_type


def test_restaurant_serializer_fields(new_restaurant):
    restaurant = new_restaurant()
    restaurant.save()

    ServiceImage.objects.create(
        image="services/gallery/restaurant.jpg",
        alt_text="img",
        content_object=restaurant,
    )

    serializer = RestaurantSerializer(instance=restaurant)
    _common_service_checks(serializer, restaurant)
    assert serializer.data["subtitle"] == restaurant.subtitle


def test_place_and_gallery_serializer(new_place):
    place = new_place()
    place.save()

    ServiceImage.objects.create(
        image="services/gallery/place.jpg", alt_text="img", content_object=place
    )

    serializer = PlaceSerializer(instance=place)
    _common_service_checks(serializer, place)
    assert serializer.data["access_type"] == place.access_type
    # ensure gallery attached_to points to this place
    assert serializer.data["gallery"][0]["attached_to"]["id"] == place.id
    assert serializer.data["gallery"][0]["attached_to"]["model_type"] == "place"


def test_stopover_serializer_fields(new_stopover):
    stopover = new_stopover()
    stopover.save()

    ServiceImage.objects.create(
        image="services/gallery/stopover.jpg", alt_text="img", content_object=stopover
    )

    serializer = StopoverSerializer(instance=stopover)
    _common_service_checks(serializer, stopover)
    assert serializer.data["arrival_city"] == stopover.arrival_city
    assert isinstance(serializer.data["pricing_guide_json"], dict)
