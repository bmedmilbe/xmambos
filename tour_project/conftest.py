# conftest.py
import pytest
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.test import Client
from django_tenants.utils import get_tenant_domain_model, get_tenant_model

from order import models as order_models
from teladoshi import models

User = get_user_model()

@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Overriding the default django_db_setup to force django-tenants
    to create the schemas during the initial test migration phase.
    """
    with django_db_blocker.unblock():
        # This forces the creation of the public schema and migrations
        connection.set_schema_to_public()


@pytest.fixture(autouse=True)
def tenant_environment(db):
    """
    Automatically creates a test tenant and switches the database
    connection context to that tenant for every test.
    """
    TenantModel = get_tenant_model()
    DomainModel = get_tenant_domain_model()

    # 1. Create the public tenant if it doesn't exist in the test DB
    public_tenant, created = TenantModel.objects.get_or_create(
        schema_name="public",
        defaults={"schema_name": "public"},  # Add other required fields here if needed
    )

    # 2. Create your test tenant
    test_tenant, created = TenantModel.objects.get_or_create(
        schema_name="test",
        defaults={"schema_name": "test"},  # Add other required fields here
    )

    # 3. Create the domain for routing IN THE PUBLIC SCHEMA
    # (Important: Domain objects are stored in the public schema for all tenants to see)
    # Set connection to public schema first
    connection.set_schema_to_public()

    domain_obj, _ = DomainModel.objects.get_or_create(
        domain="testserver", tenant=test_tenant, defaults={"is_primary": True}
    )

    # 4. Switch connection context to the test tenant schema for the actual test
    connection.set_tenant(test_tenant)

    yield test_tenant

    # 5. Clean up / Reset back to public after the test completes
    connection.set_schema_to_public()


@pytest.fixture
def client(db, tenant_environment):
    """
    Override the default pytest-django client fixture to include \
    the correct Host header.
    This ensures requests are routed to the test tenant.
    """
    test_client = Client()
    # Make all requests include the correct Host header for the test tenant
    test_client.defaults["HTTP_HOST"] = "testserver"
    return test_client


@pytest.fixture()
@pytest.mark.django_db
def new_vendor(client):
    def _new_vendor(
        company_name="Wanderlust Adventures Inc.",
        is_verified=True,
        contact_email="operations@wanderlust.com",
        contact_phone="+1-888-555-0123",
        logo="vendors/wanderlust-logo.jpg",
    ):
        vendor = models.Vendor(
            company_name=company_name,
            is_verified=is_verified,
            contact_email=contact_email,
            contact_phone=contact_phone,
            logo=logo,
        )
        return vendor

    return _new_vendor


@pytest.fixture()
@pytest.mark.django_db
def new_expedition(client, new_vendor):
    def _new_expedition(
        name="Jungle Canopy Expedition",
        description="Immersive guided expedition through pristine Amazon \
            rainforest with expert naturalists and wildlife photographers",
        price=299.99,
        image="services/covers/jungle_canopy_2026_06.jpg",
        is_active=True,
        specialization="Amazon Rainforest Wildlife",
        badge_tags="Wildlife, Photography, Conservation, Adventure, Eco-Tourism",
        mastery_text="Lead by certified naturalists with 15+ years of Amazon \
            exploration experience and conservation credentials",
    ):
        vendor = new_vendor()
        vendor.save()
        expedition = models.Expedition(
            vendor_id=vendor.id,
            name=name,
            description=description,
            price=price,
            image=image,
            is_active=is_active,
            specialization=specialization,
            badge_tags=badge_tags,
            mastery_text=mastery_text,
        )
        return expedition

    return _new_expedition


@pytest.fixture()
@pytest.mark.django_db
def new_stay(client, new_vendor):
    def _new_stay(
        name="Eco Lodge",
        description="A beautiful eco-friendly lodge",
        price=129.99,
        image="stay.jpg",
        is_active=True,
        category="Luxury Villa",
        location_detail="Amazon Rainforest",
        amenities="Swimming Pool, WiFi, Restaurant",
    ):
        vendor = new_vendor()
        vendor.save()
        stay = models.Stay(
            vendor_id=vendor.id,
            name=name,
            description=description,
            price=price,
            image=image,
            is_active=is_active,
            category=category,
            location_detail=location_detail,
            amenities=amenities,
        )
        return stay

    return _new_stay


@pytest.fixture()
@pytest.mark.django_db
def new_fleet(client, new_vendor):
    def _new_fleet(
        name="Land Rover",
        description="Rugged 4x4 adventure vehicle",
        price=99.99,
        image="fleet.jpg",
        is_active=True,
        vehicle_type="SUV",
        transmission="Automatic",
        engine="V6 Diesel",
        features="4WD, GPS, Roof Rack",
    ):
        vendor = new_vendor()
        vendor.save()
        fleet = models.Fleet(
            vendor_id=vendor.id,
            name=name,
            description=description,
            price=price,
            image=image,
            is_active=is_active,
            vehicle_type=vehicle_type,
            transmission=transmission,
            engine=engine,
            features=features,
        )
        return fleet

    return _new_fleet


@pytest.fixture()
@pytest.mark.django_db
def new_restaurant(client, new_vendor):
    def _new_restaurant(
        name="Safari Bistro",
        description="Fine dining in the wild",
        price=59.99,
        image="restaurant.jpg",
        is_active=True,
        subtitle="Culinary Excellence",
        location="Central Park",
        opening_hours="09:00-22:00",
    ):
        vendor = new_vendor()
        vendor.save()
        restaurant = models.Restaurant(
            vendor_id=vendor.id,
            name=name,
            description=description,
            price=price,
            image=image,
            is_active=is_active,
            subtitle=subtitle,
            location=location,
            opening_hours=opening_hours,
        )
        return restaurant

    return _new_restaurant


@pytest.fixture()
@pytest.mark.django_db
def new_place(client, new_vendor):
    def _new_place(
        name="Niagara Falls",
        description="Spectacular waterfall destination",
        price=0.00,
        image="place.jpg",
        is_active=True,
        access_type="Free Access",
        coordinates="43.0896,-79.0849",
    ):
        vendor = new_vendor()
        vendor.save()
        place = models.Place(
            vendor_id=vendor.id,
            name=name,
            description=description,
            price=price,
            image=image,
            is_active=is_active,
            access_type=access_type,
            coordinates=coordinates,
        )
        return place

    return _new_place


@pytest.fixture()
@pytest.mark.django_db
def new_stopover(client, new_vendor):
    def _new_stopover(
        name="Lisbon Rest Stop",
        description="Comfortable rest and transfer point",
        price=25.00,
        image="stopover.jpg",
        is_active=True,
        arrival_city="Lisbon",
        pricing_guide_json=None,
        transfer_details="Airport to city center transfer included",
    ):
        if pricing_guide_json is None:
            pricing_guide_json = {"single": 25.00, "couple": 40.00, "group": 100.00}
        vendor = new_vendor()
        vendor.save()
        stopover = models.Stopover(
            vendor_id=vendor.id,
            name=name,
            description=description,
            price=price,
            image=image,
            is_active=is_active,
            arrival_city=arrival_city,
            pricing_guide_json=pricing_guide_json,
            transfer_details=transfer_details,
        )
        return stopover

    return _new_stopover


@pytest.fixture()
@pytest.mark.django_db
def new_service_image(client, new_expedition):
    def _new_service_image(
        image="services/gallery/2026/06/jungle_gallery.jpg",
        alt_text="Scenic canopy view of Amazon rainforest",
    ):
        expedition = new_expedition()
        expedition.save()
        service_image = models.ServiceImage(
            image=image, alt_text=alt_text, content_object=expedition
        )
        return service_image

    return _new_service_image





@pytest.fixture()
@pytest.mark.django_db
def new_user(client):
    def _new_user(username="testuser", email="testuser@example.com",
                  password="password123"):
        return User.objects.create_user(username=username, email=email,
                                        password=password)
    return _new_user


@pytest.fixture()
@pytest.mark.django_db
def new_customer(client, new_user):
    def _new_customer(user=None):
        if user is None:
            user = new_user()
        return order_models.Customer(user=user)
    return _new_customer


@pytest.fixture()
@pytest.mark.django_db
def new_cart(client):
    def _new_cart():
        return order_models.Cart()
    return _new_cart


@pytest.fixture()
@pytest.mark.django_db
def new_cart_item(client, new_cart, new_vendor):
    def _new_cart_item(cart=None, content_object=None, **kwargs):
        if cart is None:
            cart = new_cart()
            cart.save()
        if content_object is None:
            # We use Vendor as our generic object target because it uses standard
            # auto-incrementing Integer IDs
            content_object = new_vendor()
            content_object.save()

        content_type = ContentType.objects.get_for_model(content_object)

        defaults = {
            "cart": cart,
            "content_type": content_type,
            "object_id": content_object.id,
            "days": 3,
            "people": 2,
            "arrive_flight": "AA123",
            "depart_flight": "AA124",
        }
        defaults.update(kwargs)
        return order_models.CartItem(**defaults)
    return _new_cart_item


@pytest.fixture()
@pytest.mark.django_db
def new_booking(client, new_user):
    def _new_booking(customer=None,
                     status=order_models.Booking.BookingStatus.PENDING,
                     revolut_url=None):

        # 1. Fallback / Parsing logic to resolve a valid Customer instance
        if customer is None:
            user_instance = new_user()
            user_instance.save()
            customer_instance, _ = order_models.Customer.objects.\
                get_or_create(user=user_instance)
        elif isinstance(customer, order_models.Customer):
            customer_instance = customer
        else:
            # If a User instance is passed directly,
            # convert it to its Customer profile relation
            customer_instance, _ = order_models.Customer.objects.\
                get_or_create(user=customer)

        # 2. Instantiate the Booking using the correct field layout tracking variable
        return order_models.Booking(
            customer=customer_instance,
            status=status,
            revolut_payment_url=revolut_url
        )
    return _new_booking


@pytest.fixture()
@pytest.mark.django_db
def new_booking_item(client, new_booking, new_vendor):
    def _new_booking_item(booking=None, content_object=None,
                          status=order_models.BookingItem.ItemStatus.PENDING, **kwargs):
        if booking is None:
            booking = new_booking()
            booking.save()
        if content_object is None:
            content_object = new_vendor()
            content_object.save()

        content_type = ContentType.objects.get_for_model(content_object)

        defaults = {
            "booking": booking,
            "content_type": content_type,
            "object_id": content_object.id,
            "days": 2,
            "people": 1,
            "status": status,
        }
        defaults.update(kwargs)
        return order_models.BookingItem(**defaults)
    return _new_booking_item


@pytest.fixture()
@pytest.mark.django_db
def new_sms_outgoing(client, new_booking):
    def _new_sms_outgoing(booking=None, phone_number="+15551234567",
                          message_text="Please confirm order", is_sent=False):
        if booking is None:
            booking = new_booking()
            booking.save()
        return order_models.SMSOutgoingQueue(
            booking=booking,
            phone_number=phone_number,
            message_text=message_text,
            is_sent_by_phone=is_sent
        )
    return _new_sms_outgoing


@pytest.fixture()
@pytest.mark.django_db
def new_payment(client, new_booking):
    def _new_payment(booking=None, amount=150.00, method="Revolut",
                     status=order_models.Payment.PaymentStatus.PENDING):
        if booking is None:
            booking = new_booking()
            booking.save()
        return order_models.Payment(
            booking=booking,
            amount=amount,
            payment_method=method,
            status=status
        )
    return _new_payment


@pytest.fixture()
@pytest.mark.django_db
def new_review(client, new_customer, new_vendor):
    def _new_review(customer=None, content_object=None, content="Excellent!", rating=5):
        if customer is None:
            customer = new_customer()
            customer.save()
        if content_object is None:
            content_object = new_vendor()
            content_object.save()

        content_type = ContentType.objects.get_for_model(content_object)
        return order_models.Review(
            customer=customer,
            content=content,
            rating=rating,
            content_type=content_type,
            object_id=content_object.id
        )
    return _new_review


@pytest.fixture()
@pytest.mark.django_db
def new_gateway_heartbeat(client):
    def _new_gateway_heartbeat(device_name="STP_Phone_Primary", battery_level=85):
        return order_models.GatewayHeartbeat(device_name=device_name,
                                             battery_level=battery_level)
    return _new_gateway_heartbeat
