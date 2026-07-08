from django.contrib import admin
from .models import GameType, Payment, Booking

admin.site.register(GameType)
admin.site.register(Payment)
admin.site.register(Booking)