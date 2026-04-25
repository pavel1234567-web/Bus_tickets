#!/usr/bin/env python
"""
Check database structure for ID uniqueness issues.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection
from tickets.models import Ticket, Booking, SeatLayout, Bus, Schedule

def check_db_structure():
    """Check database structure for issues"""
    print('=== ПРОВЕРКА СТРУКТУРЫ БАЗЫ ДАННЫХ ===')
    print()
    
    # 1. Проверяем индексы в таблицах
    print('1. Проверяем индексы в таблицах:')
    tables_to_check = ['tickets_ticket', 'tickets_booking', 'tickets_seatlayout', 'tickets_bus', 'tickets_schedule']
    
    with connection.cursor() as cursor:
        for table in tables_to_check:
            print(f'   Таблица {table}:')
            cursor.execute(f"PRAGMA index_list({table})")
            indexes = cursor.fetchall()
            
            for index in indexes:
                index_name, is_unique, table_name = index
                cursor.execute(f"PRAGMA index_info({index_name})")
                columns = cursor.fetchall()
                column_names = [col[2] for col in columns]
                print(f'     Индекс {index_name}: уникальный={is_unique}, колонки={column_names}')
            print()
    
    # 2. Проверяем дубликаты ID
    print('2. Проверяем дубликаты ID:')
    
    # Проверяем Ticket
    tickets = Ticket.objects.all()
    ticket_ids = [t.id for t in tickets]
    unique_ticket_ids = set(ticket_ids)
    if len(ticket_ids) != len(unique_ticket_ids):
        print(f'   ❌ Дубликаты ID в Ticket: {len(ticket_ids)} != {len(unique_ticket_ids)}')
        # Находим дубликаты
        from collections import Counter
        id_counts = Counter(ticket_ids)
        duplicates = [id for id, count in id_counts.items() if count > 1]
        print(f'   Дублирующиеся ID: {duplicates}')
    else:
        print(f'   ✅ ID в Ticket уникальны: {len(ticket_ids)}')
    
    # Проверяем Booking
    bookings = Booking.objects.all()
    booking_ids = [b.id for b in bookings]
    unique_booking_ids = set(booking_ids)
    if len(booking_ids) != len(unique_booking_ids):
        print(f'   ❌ Дубликаты ID в Booking: {len(booking_ids)} != {len(unique_booking_ids)}')
        from collections import Counter
        id_counts = Counter(booking_ids)
        duplicates = [id for id, count in id_counts.items() if count > 1]
        print(f'   Дублирующиеся ID: {duplicates}')
    else:
        print(f'   ✅ ID в Booking уникальны: {len(booking_ids)}')
    
    # Проверяем SeatLayout
    layouts = SeatLayout.objects.all()
    layout_ids = [l.id for l in layouts]
    unique_layout_ids = set(layout_ids)
    if len(layout_ids) != len(unique_layout_ids):
        print(f'   ❌ Дубликаты ID в SeatLayout: {len(layout_ids)} != {len(unique_layout_ids)}')
        from collections import Counter
        id_counts = Counter(layout_ids)
        duplicates = [id for id, count in id_counts.items() if count > 1]
        print(f'   Дублирующиеся ID: {duplicates}')
    else:
        print(f'   ✅ ID в SeatLayout уникальны: {len(layout_ids)}')
    
    print()
    
    # 3. Проверяем связи между таблицами
    print('3. Проверяем связи между таблицами:')
    
    # Проверяем связи Ticket -> Booking
    tickets_with_booking = Ticket.objects.filter(booking__isnull=False)
    print(f'   Ticket с Booking: {tickets_with_booking.count()}')
    
    # Проверяем связи Booking -> Schedule
    bookings_with_schedule = Booking.objects.filter(schedule__isnull=False)
    print(f'   Booking с Schedule: {bookings_with_schedule.count()}')
    
    # Проверяем связи Bus -> SeatLayout
    buses_with_layout = Bus.objects.filter(seat_layout_config__isnull=False)
    print(f'   Bus с SeatLayout: {buses_with_layout.count()}')
    
    print()
    
    # 4. Проверяем последние миграции
    print('4. Проверяем последние миграции:')
    from django.core.management import call_command
    try:
        call_command('showmigrations', '--plan', verbosity=0)
    except Exception as e:
        print(f'   Ошибка при проверке миграций: {e}')
    
    print()
    print('=== РЕКОМЕНДАЦИИ ===')
    print('1. Если есть дубликаты ID, нужно их исправить')
    print('2. Проверьте, что миграции применены корректно')
    print('3. Убедитесь, что внешние ключи работают правильно')

if __name__ == '__main__':
    check_db_structure()
