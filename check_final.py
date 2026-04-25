#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import Booking, Ticket
from django.utils import timezone

print("=== ФИНАЛЬНАЯ ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ ===")
print()

# Проверяем все бронирования
bookings = Booking.objects.all()
print(f"Всего бронирований: {bookings.count()}")

for booking in bookings:
    tickets = booking.tickets.all()
    print(f"Booking {booking.id} ({booking.booking_reference}):")
    print(f"  - Количество билетов: {tickets.count()}")
    print(f"  - Оплачено: {booking.is_paid}")
    
    if tickets.exists():
        first_ticket = tickets.first()
        print(f"  - Маршрут: {first_ticket.schedule.route.departure_city} → {first_ticket.schedule.route.arrival_city}")
        print(f"  - Место: {first_ticket.seat_number}")
        print(f"  - Цена: {first_ticket.price}")
    else:
        print(f"  - НЕТ БИЛЕТОВ!")

print()

# Проверяем все билеты
tickets_all = Ticket.objects.all()
print(f"Всего билетов: {tickets_all.count()}")

for ticket in tickets_all:
    bookings_count = ticket.booking_set.count()
    print(f"Ticket {ticket.id} (место {ticket.seat_number}):")
    print(f"  - Статус: {ticket.status}")
    print(f"  - Связанных бронирований: {bookings_count}")

print()

# Проверка проблем
problematic_bookings = Booking.objects.filter(tickets__isnull=True)
print(f"Бронирований без билетов: {problematic_bookings.count()}")

orphan_tickets = Ticket.objects.filter(booking__isnull=True)
print(f"Билетов без бронирований: {orphan_tickets.count()}")

if problematic_bookings.count() == 0 and orphan_tickets.count() == 0:
    print("✅ Все данные в порядке!")
else:
    print("⚠️ Есть проблемы с данными!")
