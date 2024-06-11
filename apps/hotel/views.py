from .models import Hotel, Staff, Guest, RoomType, Room, Booking, Payment
from .serializers import (
    HotelSerializer,
    StaffSerializer,
    GuestSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    BookingSerializer,
    PaymentSerializer,
)
from common.viewsets.base_viewsets import BaseModelViewSet
from common.viewsets.msgforcurd import MSGModelViewSet
from common.mixins import SoftDeleteMixin
from rest_framework import status, viewsets
from rest_framework.response import Response


class HotelViewSet(BaseModelViewSet, SoftDeleteMixin, MSGModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class StaffViewSet(BaseModelViewSet, SoftDeleteMixin, MSGModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class GuestViewSet(BaseModelViewSet, SoftDeleteMixin, MSGModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class RoomTypeViewSet(BaseModelViewSet, SoftDeleteMixin, MSGModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomViewSet(BaseModelViewSet, SoftDeleteMixin, MSGModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingViewSet(BaseModelViewSet, SoftDeleteMixin, MSGModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class PaymentViewSet(BaseModelViewSet, SoftDeleteMixin, MSGModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        # Get booking instance
        booking_id = request.data.get("booking")
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Set the amount from the booking total_price
        request.data["amount"] = booking.total_price

        response = super().create(request, *args, **kwargs)
        data = response.data
        data["message"] = "Payment created successfully."
        return Response(data, status=status.HTTP_201_CREATED)
