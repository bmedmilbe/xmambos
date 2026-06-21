import pytest
from django.contrib.contenttypes.models import ContentType

from order.models import (
    Booking,
    BookingItem,
    Cart,
    CartItem,
    Customer,
    GatewayHeartbeat,
    Payment,
    Review,
    SMSOutgoingQueue,
)


@pytest.mark.django_db
def test_customer(client, new_customer, new_user):
    assert Customer.objects.count() == 0

    user = new_user(username="checkout_buyer")
    customer = new_customer(user=user)
    customer.save()

    assert Customer.objects.count() == 1
    assert customer.user.username == "checkout_buyer"


@pytest.mark.django_db
def test_cart_and_items_decoupled(client, new_cart, new_cart_item, new_user):
    assert Cart.objects.count() == 0
    assert CartItem.objects.count() == 0

    cart = new_cart()
    cart.save()

    # Create a user because it uses a standard Integer ID, which fits into object_id!
    dummy_service = new_user(username="mock_service_item")
    dummy_service.save()

    # Link the Generic Foreign Key to the integer-indexed user object
    cart_item = new_cart_item(cart=cart, content_object=dummy_service, days=4, people=3)
    cart_item.save()

    assert Cart.objects.count() == 1
    assert CartItem.objects.count() == 1
    assert cart_item.days == 4
    assert cart_item.content_object == dummy_service
    assert cart_item.content_type == ContentType.objects.get_for_model(
        dummy_service.__class__)


@pytest.mark.django_db
def test_booking_and_booking_items_decoupled(client, new_booking,
                                             new_booking_item,
                                             new_customer,
                                             new_user):
    assert Booking.objects.count() == 0
    assert BookingItem.objects.count() == 0

    user = new_user(username="traveler_one")
    customer_profile = new_customer(user=user)
    customer_profile.save()

    # FIXED: Change parameter target to match 'customer' as defined in conftest.py
    booking = new_booking(customer=customer_profile,
                          status=Booking.BookingStatus.AWAITING_SMS)
    booking.save()

    # Create another user instance to act as our integer-indexed service item
    dummy_service = new_user(username="mock_booked_service")
    dummy_service.save()

    # Link the Generic Foreign Key safely
    booking_item = new_booking_item(booking=booking,
                                    content_object=dummy_service,
                                    days=5)
    booking_item.save()

    assert Booking.objects.count() == 1
    assert BookingItem.objects.count() == 1
    assert booking_item.booking == booking
    assert booking_item.content_object == dummy_service


@pytest.mark.django_db
def test_sms_outgoing_queue(client, new_booking, new_sms_outgoing, new_customer):
    assert SMSOutgoingQueue.objects.count() == 0

    customer_profile = new_customer()
    customer_profile.save()

    # FIXED: Change parameter target to match 'customer' as defined in conftest.py
    booking = new_booking(customer=customer_profile)
    booking.save()

    sms = new_sms_outgoing(booking=booking, phone_number="+351912345678", is_sent=True)
    sms.save()

    assert SMSOutgoingQueue.objects.count() == 1
    assert sms.is_sent_by_phone is True


@pytest.mark.django_db
def test_payment(client, new_booking, new_payment, new_customer):
    assert Payment.objects.count() == 0

    customer_profile = new_customer()
    customer_profile.save()

    # FIXED: Change parameter target to match 'customer' as defined in conftest.py
    booking = new_booking(customer=customer_profile)
    booking.save()

    payment = new_payment(booking=booking,
                          amount=599.95,
                          status=Payment.PaymentStatus.CONFIRMED)
    payment.save()

    assert Payment.objects.count() == 1
    assert payment.status == Payment.PaymentStatus.CONFIRMED


@pytest.mark.django_db
def test_review_generic_relation_decoupled(client, new_customer, new_review):
    assert Review.objects.count() == 0

    customer = new_customer()
    customer.save()

    # Link the review generic foreign key back to the customer profile
    review = new_review(customer=customer, content_object=customer, rating=5)
    review.save()

    assert Review.objects.count() == 1
    assert review.service == customer
    assert review.content_type == ContentType.objects.get_for_model(Customer)


@pytest.mark.django_db
def test_gateway_heartbeat(client, new_gateway_heartbeat):
    assert GatewayHeartbeat.objects.count() == 0

    heartbeat = new_gateway_heartbeat(device_name="STP_Phone_Backup", battery_level=42)
    heartbeat.save()

    assert GatewayHeartbeat.objects.count() == 1
    assert heartbeat.battery_level == 42
