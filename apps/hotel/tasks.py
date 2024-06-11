from celery import shared_task
from django.utils import timezone
from apps.hotel.models import Room, Booking
import os
import binascii


@shared_task
def update_room_status():
    today = timezone.now().date()
    expired_bookings = Booking.objects.filter(
        check_out_date__lt=today, room__status=Room.OCCUPIED
    )

    for booking in expired_bookings:
        room = booking.room
        room.status = Room.AVAILABLE
        room.save()


# def generate_unique_number(prefix, length, model, field):
#     while True:
#         random_bytes = os.urandom(binascii(length / 2))
#         unique_code = (
#             prefix
#             + binascii.hexlify(random_bytes).decode("utf-8")[:length].upper()
#         )
#         if not model.objects.filter(**{field: unique_code}).exists():
#             return unique_code
