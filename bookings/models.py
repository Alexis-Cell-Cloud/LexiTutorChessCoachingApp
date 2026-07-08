from django.db import models
from django.conf import settings
from datetime import date, timedelta
from decimal import Decimal


def calculate_discount_percent(session_date) : 
    days_ahead = (session_date - date.today()).days
    if days_ahead >= 270:
        return Decimal('20')
    elif days_ahead >= 180:
        return Decimal('15')
    elif days_ahead >= 90:
        return Decimal('10')
    elif days_ahead >= 30:
        return Decimal('5')
    return Decimal('0')


def calculate_surcharge_percent(actual_duration_hours):
    standard = Decimal('3')
    if actual_duration_hours <= standard:
        return Decimal('0')
    overtime_hours = actual_duration_hours - standard
    import math
    full_extra_hours = math.ceil(overtime_hours)
    return Decimal('20') * full_extra_hours


class GameType(models.Model):
    class Tier(models.TextChoices):
        FULL = 'FULL', 'Full Rate'
        MID = 'MID', 'Mid Tier'
        LOWER = 'LOWER', 'Lower Tier'

    class GameName(models.TextChoices):
        CHESS = 'CHESS', 'Chess'
        SUDOKU = 'SUDOKU', 'Sudoku'
        SCRAMBLE = 'SCRAMBLE', 'Scramble'
        CHECKERS = 'CHECKERS', 'Checkers'
        WHOT = 'WHOT', 'Whot'
        LUDO = 'LUDO', 'Ludo'

    name = models.CharField(max_length=20, choices=GameName.choices, unique=True)
    tier = models.CharField(max_length=10, choices=Tier.choices)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.get_name_display()
    
class Booking(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    game = models.ForeignKey(
        GameType,
        on_delete=models.PROTECT,
        related_name='bookings'
    )

    booking_made_at = models.DateTimeField(auto_now_add=True)
    session_date = models.DateField()
    session_start_time = models.TimeField()
    address = models.CharField(max_length=255)

    STANDARD_DURATION_HOURS = 3
    actual_duration_hours = models.DecimalField(
        max_digits=4, decimal_places=2,
        default=STANDARD_DURATION_HOURS
    )

    is_streak = models.BooleanField(default=False)
    streak_group_id = models.UUIDField(null=True, blank=True)

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'

    payment_status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    surcharge_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.client.username} - {self.game.name} on {self.session_date}"
    
    class Meta:
        ordering = ['session_date', 'session_start_time']

class Payment(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    reference = models.CharField(max_length=100, unique=True)
    access_code = models.CharField(max_length=100, blank=True)

    amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference} - {self.status}"