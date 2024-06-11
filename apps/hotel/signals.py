from django.db.models.signals import post_save, pre_delete, pre_save
from .models import Booking, Room, Payment
from django.dispatch import Signal
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=Booking)
def update_room_status_on_booking_create(sender, instance, created, **kwargs):
    if created:
        instance.room.status = Room.OCCUPIED
        instance.room.save()


@receiver(pre_delete, sender=Booking)
def update_room_status_on_booking_delete(sender, instance, **kwargs):
    instance.room.status = Room.AVAILABLE
    instance.room.save()


@receiver(post_save, sender=Booking)
def update_room_status_on_dates_change(sender, instance, **kwargs):
    if instance.check_out_date < timezone.now().date():
        instance.room.status = Room.AVAILABLE
        instance.room.save()


@receiver(pre_save, sender=Payment)
def sync_payment_with_booking(sender, instance, **kwargs):
    # Ensure the payment amount matches the booking total price
    instance.amount = instance.booking.total_price


@receiver(post_save, sender=Payment)
def update_booking_total_price(sender, instance, created, **kwargs):
    if created:
        booking = instance.booking
        booking.total_price = instance.amount
        booking.save()


@receiver(pre_delete, sender=Payment)
def update_booking_total_price_on_delete(sender, instance, **kwargs):
    booking = instance.booking
    booking.total_price -= instance.amount
    booking.save()


# Define custom signals
post_create_signal = Signal()
post_update_signal = Signal()
post_delete_signal = Signal()


"""
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import Booking, Payment
from .utils import handle_booking_and_payment_tasks

@receiver(post_save, sender=Booking)
def handle_booking_create_and_update(sender, instance, created, **kwargs):
    handle_booking_and_payment_tasks(booking_instance=instance, created=created)

@receiver(pre_delete, sender=Booking)
def handle_booking_delete(sender, instance, **kwargs):
    handle_booking_and_payment_tasks(booking_instance=instance, deleted=True)

@receiver(pre_save, sender=Payment)
def handle_payment_sync(sender, instance, **kwargs):
    # Ensure the payment amount matches the booking total price
    instance.amount = instance.booking.total_price

@receiver(post_save, sender=Payment)
def handle_payment_create(sender, instance, created, **kwargs):
    handle_booking_and_payment_tasks(payment_instance=instance, created=created)

@receiver(pre_delete, sender=Payment)
def handle_payment_delete(sender, instance, **kwargs):
    handle_booking_and_payment_tasks(payment_instance=instance, deleted=True)
"""
