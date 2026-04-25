#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import Booking, Ticket

print("=== FINAL INTEGRITY CHECK ===")
print()

# Check all bookings
bookings = Booking.objects.all()
print(f"Total bookings: {bookings.count()}")

for booking in bookings:
    tickets = booking.tickets.all()
    print(f"Booking {booking.id} ({booking.booking_reference}):")
    print(f"  - Tickets count: {tickets.count()}")
    print(f"  - Is paid: {booking.is_paid}")
    
    if tickets.exists():
        first_ticket = tickets.first()
        print(f"  - Route: {first_ticket.schedule.route.departure_city} to {first_ticket.schedule.route.arrival_city}")
        print(f"  - Seat: {first_ticket.seat_number}")
        print(f"  - Price: {first_ticket.price}")
    else:
        print(f"  - NO TICKETS!")

print()

# Check all tickets
tickets_all = Ticket.objects.all()
print(f"Total tickets: {tickets_all.count()}")

for ticket in tickets_all:
    bookings_count = ticket.booking_set.count()
    print(f"Ticket {ticket.id} (seat {ticket.seat_number}):")
    print(f"  - Status: {ticket.status}")
    print(f"  - Related bookings: {bookings_count}")

print()

# Check for problems
problematic_bookings = Booking.objects.filter(tickets__isnull=True)
print(f"Bookings without tickets: {problematic_bookings.count()}")

orphan_tickets = Ticket.objects.filter(booking__isnull=True)
print(f"Tickets without bookings: {orphan_tickets.count()}")

if problematic_bookings.count() == 0 and orphan_tickets.count() == 0:
    print("SUCCESS: All data is correct!")
else:
    print("WARNING: There are data integrity issues!")
