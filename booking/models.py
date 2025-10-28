from django.db import models
from django.db.models import UniqueConstraint

from config import settings


class Event(models.Model):
    """Event model"""
    name = models.CharField(max_length=255, blank=True)
    total_seats = models.IntegerField()
    def __str__(self):
        return self.name


class Booking(models.Model):
    """Booking model"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="booking_user_set",
        null=True,
        blank=True
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name="booking_event_set")
    created_at = models.DateTimeField(auto_now_add=True)
    constraints = [
            UniqueConstraint(fields=['user', 'event'], name='unique_booking_user_event')
        ]

