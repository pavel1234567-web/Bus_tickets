#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import Booking, Ticket

# Check recent booking and ticket data
booking = Booking.objects.order_by('-created_at').first()
if booking:
    print(f'Booking {booking.booking_reference}:')
    print(f'  First Name: "{booking.first_name}"')
    print(f'  Last Name: "{booking.last_name}"')
    print(f'  Email: "{booking.email}"')
    print(f'  Phone: "{booking.phone}"')
    print(f'  Total Price: {booking.total_price}')
    print(f'  Tickets: {booking.tickets.count()}')
    
    for ticket in booking.tickets.all():
        print(f'    Ticket {ticket.seat_number}:')
        print(f'      Price: {ticket.price}')
        print(f'      Status: {ticket.status}')
        print(f'      Schedule: {ticket.schedule}')
else:
    print('No bookings found')
