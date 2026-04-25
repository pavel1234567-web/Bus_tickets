#!/usr/bin/env python
"""
Check database structure for PostgreSQL.
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

def check_db_postgres():
    """Check database structure for PostgreSQL"""
    print('=== ПРОВЕРКА СТРУКТУРЫ БАЗЫ ДАННЫХ (PostgreSQL) ===')
    print()
    
    # 1. Проверяем дубликаты ID в таблицах
    print('1. Проверяем дубликаты ID:')
    
    # Проверяем Ticket
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, COUNT(*) FROM tickets_ticket GROUP BY id HAVING COUNT(*) > 1")
        ticket_duplicates = cursor.fetchall()
        if ticket_duplicates:
            print(f'   ❌ Дубликаты ID в Ticket: {ticket_duplicates}')
        else:
            print(f'   ✅ ID в Ticket уникальны')
        
        # Проверяем Booking
        cursor.execute("SELECT id, COUNT(*) FROM tickets_booking GROUP BY id HAVING COUNT(*) > 1")
        booking_duplicates = cursor.fetchall()
        if booking_duplicates:
            print(f'   ❌ Дубликаты ID в Booking: {booking_duplicates}')
        else:
            print(f'   ✅ ID в Booking уникальны')
        
        # Проверяем SeatLayout
        cursor.execute("SELECT id, COUNT(*) FROM tickets_seatlayout GROUP BY id HAVING COUNT(*) > 1")
        layout_duplicates = cursor.fetchall()
        if layout_duplicates:
            print(f'   ❌ Дубликаты ID в SeatLayout: {layout_duplicates}')
        else:
            print(f'   ✅ ID в SeatLayout уникальны')
    
    print()
    
    # 2. Проверяем индексы
    print('2. Проверяем индексы:')
    with connection.cursor() as cursor:
        # Получаем все индексы для таблиц
        cursor.execute("""
            SELECT schemaname, tablename, indexname, indexdef 
            FROM pg_indexes 
            WHERE tablename IN ('tickets_ticket', 'tickets_booking', 'tickets_seatlayout', 'tickets_bus', 'tickets_schedule')
            ORDER BY tablename, indexname
        """)
        indexes = cursor.fetchall()
        
        for schema, table, index_name, index_def in indexes:
            print(f'   {table}: {index_name}')
            print(f'     {index_def}')
        print()
    
    # 3. Проверяем связи
    print('3. Проверяем связи:')
    with connection.cursor() as cursor:
        # Проверяем внешние ключи
        cursor.execute("""
            SELECT 
                tc.table_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name 
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_name IN ('tickets_ticket', 'tickets_booking', 'tickets_seatlayout', 'tickets_bus', 'tickets_schedule')
        """)
        foreign_keys = cursor.fetchall()
        
        for table, column, foreign_table, foreign_column in foreign_keys:
            print(f'   {table}.{column} -> {foreign_table}.{foreign_column}')
        print()
    
    # 4. Проверяем последовательности для ID
    print('4. Проверяем последовательности для ID:')
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
    
    # 5. Проверяем текущие значения ID
    print('5. Текущие значения ID:')
    print(f'   Ticket: {Ticket.objects.count()} записей, max ID: {Ticket.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0}')
    print(f'   Booking: {Booking.objects.count()} записей, max ID: {Booking.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0}')
    print(f'   SeatLayout: {SeatLayout.objects.count()} записей, max ID: {SeatLayout.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0}')
    print(f'   Bus: {Bus.objects.count()} записей, max ID: {Bus.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0}')
    print(f'   Schedule: {Schedule.objects.count()} записей, max ID: {Schedule.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0}')
    print()
    
    print('=== ГОТОВО! ===')

if __name__ == '__main__':
    from django.db import models
    check_db_postgres()
