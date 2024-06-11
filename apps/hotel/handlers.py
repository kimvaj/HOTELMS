# apps/hotel/handlers.py
from django.dispatch import receiver
from .signals import post_create_signal, post_update_signal, post_delete_signal


@receiver(post_create_signal)
def post_create_handler(sender, instance, created, **kwargs):
    if created:
        print(f"Instance created: {instance}")


@receiver(post_update_signal)
def post_update_handler(sender, instance, **kwargs):
    print(f"Instance updated: {instance}")


@receiver(post_delete_signal)
def post_delete_handler(sender, instance, **kwargs):
    print(f"Instance deleted: {instance}")
