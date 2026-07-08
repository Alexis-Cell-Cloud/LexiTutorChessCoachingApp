from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_view, name='booking'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('available-slots/', views.available_slots, name='available_slots'),
    path('initialize-payment/<int:booking_id>/', views.initialize_payment, name='initialize_payment'),
    path('verify-payment/<int:booking_id>/', views.verify_payment, name='verify_payment'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]