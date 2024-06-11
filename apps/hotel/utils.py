from django.utils import timezone
from .models import Room, Payment


def handle_booking_and_payment_tasks(
    booking_instance=None, payment_instance=None, created=False, deleted=False
):
    if booking_instance:
        # Update room status based on booking creation, deletion, or date change
        if created:
            booking_instance.room.status = Room.OCCUPIED
        elif deleted:
            booking_instance.room.status = Room.AVAILABLE
        elif booking_instance.check_out_date < timezone.now().date():
            booking_instance.room.status = Room.AVAILABLE
        booking_instance.room.save()

    if payment_instance:
        # Sync payment amount with booking total price and update booking total price
        if created:
            payment_instance.amount = payment_instance.booking.total_price
            booking_instance = payment_instance.booking
            booking_instance.total_price = payment_instance.amount
            booking_instance.save()
        elif deleted:
            booking_instance = payment_instance.booking
            booking_instance.total_price -= payment_instance.amount
            booking_instance.save()
