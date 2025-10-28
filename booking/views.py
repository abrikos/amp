from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from booking.models import Booking, Event
from booking.serializers import BookingSerializer, EventSerializer



# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    """Event REST"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

@method_decorator(name='list', decorator=swagger_auto_schema(
            operation_description="Retrieve a list of all Booking instances.",
            operation_summary="Get all Bookings"
        ))

@method_decorator(name='create', decorator=swagger_auto_schema(
            operation_description="Create Booking instance.",
            operation_summary="Register Booking"
        ))

@method_decorator(name='retrieve', decorator=swagger_auto_schema(
            operation_description="View Booking instance.",
            operation_summary="View Booking by id"
        ))

@method_decorator(name='update', decorator=swagger_auto_schema(
            operation_description="Update Booking instance.",
            operation_summary="Update Booking by id"
        ))

@method_decorator(name='partial_update', decorator=swagger_auto_schema(
            operation_description="Update some fields of Booking instance.",
            operation_summary="Update Booking attributes by id"
        ))

@method_decorator(name='destroy', decorator=swagger_auto_schema(
            operation_description="Delete Booking instance.",
            operation_summary="Delete Booking by id"
        ))

@method_decorator(name='reserve', decorator=swagger_auto_schema(
            operation_description="Reserve user on Event. User can reserve one event only once",
            operation_summary="Reserve Event for user"
        ))



class BookingViewSet(viewsets.ModelViewSet):
    """Booking REST"""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permissions = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def reserve(self, request):
        event = Event.objects.get(pk=request.data["event_id"])
        try:
            exists_booking = Booking.objects.get(event=event, user=request.user)
        except Booking.DoesNotExist:
            exists_booking = None
        if exists_booking:
            return HttpResponseBadRequest("Booking already registered on this booking")
        else:
            Booking.objects.create(event=event, user=request.user)
            return Response({})