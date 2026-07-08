from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta, datetime
from decimal import Decimal
from .forms import BookingForm
from .models import Booking, Payment, calculate_discount_percent, calculate_surcharge_percent
from django.http import JsonResponse
import requests
from django.conf import settings
from django.utils import timezone
from django.db import models

@login_required
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user

            # Daily limit check: max 4 bookings/day
            same_day_count = Booking.objects.filter(
                client=request.user,
                session_date=booking.session_date
            ).count()
            if same_day_count >= 4:
                messages.error(request, "You've reached the maximum of 4 bookings for this day.")
                return render(request, 'bookings/booking.html', {'form': form})

            # Slot overlap check: 6-hour block (5hr max session + 1hr buffer)
            new_start = datetime.combine(booking.session_date, booking.session_start_time)
            new_end = new_start + timedelta(hours=6)

            existing_bookings = Booking.objects.filter(
                client=request.user,
                session_date=booking.session_date
            )
            for existing in existing_bookings:
                existing_start = datetime.combine(existing.session_date, existing.session_start_time)
                existing_end = existing_start + timedelta(hours=6)
                if new_start < existing_end and existing_start < new_end:
                    messages.error(request, "This time slot overlaps with another booking.")
                    return render(request, 'bookings/booking.html', {'form': form})

            # Price calculation
            discount = calculate_discount_percent(booking.session_date)
            surcharge = calculate_surcharge_percent(booking.actual_duration_hours)
            base_price = booking.game.base_price

            price_after_discount = base_price * (Decimal('1') - discount / Decimal('100'))
            final_price = price_after_discount * (Decimal('1') + surcharge / Decimal('100'))

            booking.discount_percent = discount
            booking.surcharge_percent = surcharge
            booking.final_price = final_price

            booking.save()
            return redirect('initialize_payment', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'bookings/booking.html', {'form': form})

@login_required
def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id, client=request.user)
    return render(request, 'bookings/confirmation.html', {'booking': booking})

@login_required
def initialize_payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id, client=request.user)

    amount_in_kobo = int(booking.final_price * 100)

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        'email': booking.client.email,
        'amount': amount_in_kobo,
        'callback_url': request.build_absolute_uri(f'/booking/verify-payment/{booking.id}/'),
    }

    response = requests.post(
        'https://api.paystack.co/transaction/initialize',
        headers=headers,
        json=data
    )

    response_data = response.json()

    if response_data.get('status'):
        payment, created = Payment.objects.update_or_create(
            booking=booking,
            defaults={
                'reference': response_data['data']['reference'],
                'access_code': response_data['data']['access_code'],
                'amount': booking.final_price,
                'status': 'PENDING',
            }
        )
        return redirect(response_data['data']['authorization_url'])
    else:
        messages.error(request, 'Payment initialization failed. Please try again.')
        return redirect('booking_confirmation', booking_id=booking.id)

@login_required
def verify_payment(request, booking_id):
    reference = request.GET.get('reference')

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }

    response = requests.get(
        f'https://api.paystack.co/transaction/verify/{reference}',
        headers=headers
    )

    response_data = response.json()

    if response_data.get('status') and response_data['data']['status'] == 'success':
        booking = Booking.objects.get(id=booking_id, client=request.user)
        payment = booking.payment

        payment.status = 'SUCCESS'
        payment.paid_at = response_data['data']['paid_at']
        payment.save()

        booking.payment_status = 'PAID'
        booking.save()

        messages.success(request, 'Payment successful! Your booking is confirmed.')
    else:
        messages.error(request, 'Payment verification failed. Please contact support.')

    return redirect('booking_confirmation', booking_id=booking_id)

def available_slots(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'date is required'}, status=400)

    session_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    expiry_cutoff = timezone.now() - timedelta(minutes=30)

    bookings = Booking.objects.filter(session_date=session_date).filter(
        models.Q(payment_status='PAID') |
        models.Q(payment_status='PENDING', booking_made_at__gte=expiry_cutoff)
    )

    blocked_hours = set()
    for booking in bookings:
        start = datetime.combine(session_date, booking.session_start_time)
        block_start = start - timedelta(hours=1)
        block_end = start + timedelta(hours=5)

        hour = block_start
        while hour < block_end:
            blocked_hours.add(hour.strftime('%H:%M'))
            hour += timedelta(hours=1)

    return JsonResponse({'blocked_hours': list(blocked_hours)})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(client=request.user).order_by('-session_date')
    return render(request, 'bookings/booking_session_history.html', {'bookings': bookings})