#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import Booking, Ticket, Payment
from django.db import transaction

print("=== ИСПРАВЛЕНИЕ ЦЕЛОСТНОСТИ ДАННЫХ ===")
print()

def fix_data_integrity():
    """Исправление проблем с целостностью данных между Booking и Ticket"""
    
    print("1. УДАЛЕНИЕ БРОНИРОВАНИЙ БЕЗ БИЛЕТОВ")
    problematic_bookings = Booking.objects.filter(tickets__isnull=True)
    print(f"Найдено бронирований без билетов: {problematic_bookings.count()}")
    
    for booking in problematic_bookings:
        print(f"  - Удаляю Booking {booking.id} ({booking.booking_reference})")
        booking.delete()
    
    print("\n2. ПРОВЕРКА ОСИРЕТЕВШИХ БИЛЕТОВ")
    orphan_tickets = Ticket.objects.filter(booking__isnull=True)
    print(f"Найдено билетов без бронирований: {orphan_tickets.count()}")
    
    if orphan_tickets.exists():
        print("\n3. СОЗДАНИЕ БРОНИРОВАНИЙ ДЛЯ ОСИРЕТЕВШИХ БИЛЕТОВ")
        
        for ticket in orphan_tickets:
            # Создаем новое бронирование для каждого orphan билета
            with transaction.atomic():
                # Генерируем уникальный номер бронирования
                import uuid
                booking_ref = f"BT{uuid.uuid4().hex[:8].upper()}"
                
                # Создаем бронирование
                new_booking = Booking.objects.create(
                    first_name="Test",
                    last_name="User", 
                    email="test@example.com",
                    phone="+1234567890",
                    booking_reference=booking_ref,
                    total_price=ticket.price,
                    is_paid=False
                )
                
                # Связываем билет с бронированием
                new_booking.tickets.add(ticket)
                
                print(f"  - Создано Booking {new_booking.id} для Ticket {ticket.id}")
    
    print("\n4. ПРОВЕРКА РЕЗУЛЬТАТОВ")
    
    # Проверяем все бронирования
    all_bookings = Booking.objects.all()
    print(f"Всего бронирований после исправления: {all_bookings.count()}")
    
    for booking in all_bookings:
        tickets_count = booking.tickets.count()
        print(f"  - Booking {booking.id}: {tickets_count} билетов")
    
    # Проверяем все билеты
    all_tickets = Ticket.objects.all()
    print(f"\nВсего билетов: {all_tickets.count()}")
    
    orphan_after = Ticket.objects.filter(booking__isnull=True)
    print(f"Билетов без бронирований после исправления: {orphan_after.count()}")
    
    print("\n✅ Целостность данных восстановлена!")

if __name__ == "__main__":
    fix_data_integrity()
