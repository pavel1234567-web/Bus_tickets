#!/usr/bin/env python
"""
Simple database check for ID uniqueness.
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

def check_db_simple():
    """Simple database check"""
    print('=== ПРОСТАЯ ПРОВЕРКА БАЗЫ ДАННЫХ ===')
    print()
    
    # 1. Проверяем дубликаты ID
    print('1. Проверяем дубликаты ID:')
    
    with connection.cursor() as cursor:
        # Ticket
        cursor.execute("SELECT id, COUNT(*) FROM tickets_ticket GROUP BY id HAVING COUNT(*) > 1")
        ticket_duplicates = cursor.fetchall()
        if ticket_duplicates:
            print(f'   - Дубликаты ID в Ticket: {ticket_duplicates}')
        else:
            print(f'   + ID в Ticket уникальны')
        
        # Booking
        cursor.execute("SELECT id, COUNT(*) FROM tickets_booking GROUP BY id HAVING COUNT(*) > 1")
        booking_duplicates = cursor.fetchall()
        if booking_duplicates:
            print(f'   - Дубликаты ID в Booking: {booking_duplicates}')
        else:
            print(f'   + ID в Booking уникальны')
        
        # SeatLayout
        cursor.execute("SELECT id, COUNT(*) FROM tickets_seatlayout GROUP BY id HAVING COUNT(*) > 1")
        layout_duplicates = cursor.fetchall()
        if layout_duplicates:
            print(f'   - Дубликаты ID в SeatLayout: {layout_duplicates}')
        else:
            print(f'   + ID в SeatLayout уникальны')
    
    print()
    
    # 2. Проверяем количество записей и максимальные ID
    print('2. Количество записей и максимальные ID:')
    from django.db import models
    
    tables = [
        ('Ticket', Ticket),
        ('Booking', Booking),
        ('SeatLayout', SeatLayout),
        ('Bus', Bus),
        ('Schedule', Schedule)
    ]
    
    for name, model in tables:
        count = model.objects.count()
        max_id = model.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
        print(f'   {name}: {count} записей, max ID: {max_id}')
        
        # Проверяем, есть ли несоответствие
        if count != max_id and max_id > 0:
            print(f'     ! Несоответствие: count={count} != max_id={max_id}')
    
    print()
    
    # 3. Проверяем последовательности
    print('3. Проверяем последовательности:')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                table_name, 
                column_name,
                column_default
            FROM information_schema.columns 
            WHERE table_name IN ('tickets_ticket', 'tickets_booking', 'tickets_seatlayout', 'tickets_bus', 'tickets_schedule')
                AND column_name = 'id'
        """)
        sequences = cursor.fetchall()
        
        for table, column, default_val in sequences:
            print(f'   {table}.{column}: {default_val}')
    
    print()
    
    # 4. Проверяем последние созданные записи
    print('4. Последние созданные записи:')
    for name, model in tables:
        if model.objects.exists():
            latest = model.objects.latest('id')
            print(f'   {name}: ID={latest.id}, создан={getattr(latest, 'created_at', 'N/A')}')

if __name__ == '__main__':
    check_db_simple()
