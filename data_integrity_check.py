#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import Booking, Ticket, Payment
from datetime import datetime, timedelta

def check_data_integrity():
    """Проверка целостности данных между Booking и Ticket"""
    
    print("=== ПРОВЕРКА ЦЕЛОСТНОСТИ ДАННЫХ ===")
    print(f"Время проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    issues_found = []
    
    # 1. Проверяем бронирования без билетов
    bookings_without_tickets = Booking.objects.filter(tickets__isnull=True)
    if bookings_without_tickets.exists():
        issues_found.append(f"Бронирований без билетов: {bookings_without_tickets.count()}")
        for booking in bookings_without_tickets:
            issues_found.append(f"  - Booking {booking.id} ({booking.booking_reference})")
    
    # 2. Проверяем билеты без бронирований
    tickets_without_bookings = Ticket.objects.filter(booking__isnull=True)
    if tickets_without_bookings.exists():
        issues_found.append(f"Билетов без бронирований: {tickets_without_bookings.count()}")
        for ticket in tickets_without_bookings:
            issues_found.append(f"  - Ticket {ticket.id} (место {ticket.seat_number})")
    
    # 3. Проверяем старые неоплаченные бронирования
    old_unpaid_bookings = Booking.objects.filter(
        is_paid=False,
        created_at__lt=datetime.now() - timedelta(minutes=10)
    )
    if old_unpaid_bookings.exists():
        issues_found.append(f"Старых неоплаченных бронирований (>10 мин): {old_unpaid_bookings.count()}")
        for booking in old_unpaid_bookings:
            age = datetime.now() - booking.created_at.replace(tzinfo=None)
            issues_found.append(f"  - Booking {booking.id} (возраст: {age.seconds//60} мин)")
    
    # 4. Проверка статистики
    total_bookings = Booking.objects.count()
    total_tickets = Ticket.objects.count()
    paid_bookings = Booking.objects.filter(is_paid=True).count()
    
    print(f"СТАТИСТИКА:")
    print(f"  - Всего бронирований: {total_bookings}")
    print(f"  - Оплаченных бронирований: {paid_bookings}")
    print(f"  - Всего билетов: {total_tickets}")
    print()
    
    if issues_found:
        print("⚠️  НАЙДЕНЫ ПРОБЛЕМЫ:")
        for issue in issues_found:
            print(f"  {issue}")
        return False
    else:
        print("✅ Проблем не найдено. Целостность данных в порядке.")
        return True

if __name__ == "__main__":
    check_data_integrity()
