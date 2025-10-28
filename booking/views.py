from django.http import HttpResponseBadRequest
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
            return HttpResponseBadRequest("User already registered on this booking")
        else:
            Booking.objects.create(event=event, user=request.user)
            return Response({})