#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import Booking, Ticket

print("=== Проверка связей между бронированиями и билетами ===")
print()

# Проверяем все бронирования
bookings = Booking.objects.all()
print(f"Всего бронирований: {bookings.count()}")

for booking in bookings:
    tickets = booking.tickets.all()
    print(f"\nBooking {booking.id} ({booking.booking_reference}):")
    print(f"  - Количество билетов: {tickets.count()}")
    print(f"  - Оплачено: {booking.is_paid}")
    
    if tickets.exists():
        first_ticket = tickets.first()
        print(f"  - Первый билет: {first_ticket}")
        print(f"  - Расписание: {first_ticket.schedule}")
        print(f"  - Маршрут: {first_ticket.schedule.route if first_ticket.schedule else 'Нет'}")
    else:
        print(f"  - НЕТ СВЯЗАННЫХ БИЛЕТОВ!")

print("\n=== Проверка всех билетов ===")
tickets_all = Ticket.objects.all()
print(f"Всего билетов: {tickets_all.count()}")

for ticket in tickets_all:
    print(f"Ticket {ticket.id}:")
    print(f"  - Место: {ticket.seat_number}")
    print(f"  - Статус: {ticket.status}")
    print(f"  - Booking reference: {ticket.booking_reference}")
    print(f"  - Расписание: {ticket.schedule}")
    print(f"  - Связанные бронирования: {ticket.booking_set.count()}")

print("\n=== Проверка проблемных бронирований ===")
problematic_bookings = Booking.objects.filter(tickets__isnull=True)
print(f"Бронирований без билетов: {problematic_bookings.count()}")

for booking in problematic_bookings:
    print(f"Booking {booking.id} ({booking.booking_reference}) - НЕТ БИЛЕТОВ")
