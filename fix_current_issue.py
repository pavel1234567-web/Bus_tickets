#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import Booking, Ticket

print("=== FIXING CURRENT BOOKING ISSUES ===")
print()

# Find and delete problematic bookings
problematic_bookings = Booking.objects.filter(tickets__isnull=True)
print(f"Found {problematic_bookings.count()} bookings without tickets")

for booking in problematic_bookings:
    print(f"Deleting Booking {booking.id} ({booking.booking_reference})")
    booking.delete()

print()
print("Checking final state:")

# Check all bookings
all_bookings = Booking.objects.all()
print(f"Total bookings after cleanup: {all_bookings.count()}")

for booking in all_bookings:
    tickets_count = booking.tickets.count()
    print(f"Booking {booking.id}: {tickets_count} tickets")

# Check for problems
bookings_without_tickets = Booking.objects.filter(tickets__isnull=True)
print(f"Bookings without tickets: {bookings_without_tickets.count()}")

if bookings_without_tickets.count() == 0:
    print("SUCCESS: All bookings have tickets!")
else:
    print("WARNING: Still have bookings without tickets!")
