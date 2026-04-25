#!/usr/bin/env python
"""
Fix PostgreSQL sequences to match actual data.
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

def fix_sequences():
    """Fix PostgreSQL sequences"""
    print('=== ИСПРАВЛЕНИЕ ПОСЛЕДОВАТЕЛЬНОСТЕЙ POSTGRESQL ===')
    print()
    
    tables = [
        ('tickets_ticket', Ticket),
        ('tickets_booking', Booking),
        ('tickets_seatlayout', SeatLayout),
        ('tickets_bus', Bus),
        ('tickets_schedule', Schedule)
    ]
    
    with connection.cursor() as cursor:
        for table_name, model in tables:
            print(f'Исправляем последовательность для {table_name}:')
            
            # Получаем максимальный ID
            cursor.execute(f"SELECT MAX(id) FROM {table_name}")
            max_id = cursor.fetchone()[0]
            
            if max_id is None:
                max_id = 0
            
            print(f'   Текущий max ID: {max_id}')
            
            # Получаем имя последовательности
            cursor.execute(f"""
                SELECT pg_get_serial_sequence('{table_name}', 'id')
            """)
            sequence_name = cursor.fetchone()[0]
            
            if sequence_name:
                print(f'   Последовательность: {sequence_name}')
                
                # Устанавливаем новое значение последовательности
                new_value = max_id + 1
                cursor.execute(f"""
                    SELECT setval('{sequence_name}', {new_value}, true)
                """)
                
                # Проверяем результат
                cursor.execute(f"""
                    SELECT last_value FROM {sequence_name}
                """)
                last_value = cursor.fetchone()[0]
                
                print(f'   Установлено значение: {last_value}')
                print(f'   + Исправлено!')
            else:
                print(f'   - Последовательность не найдена')
            
            print()
    
    # Проверяем результат
    print('Проверяем результат:')
    for table_name, model in tables:
        count = model.objects.count()
        cursor.execute(f"SELECT MAX(id) FROM {table_name}")
        max_id = cursor.fetchone()[0] or 0
        
        if count == max_id or max_id == 0:
            print(f'   + {table_name}: count={count}, max_id={max_id}')
        else:
            print(f'   - {table_name}: count={count}, max_id={max_id} (все еще проблема)')
    
    print()
    print('=== ГОТОВО! ===')
    print('Последовательности исправлены.')
    print('Теперь новые записи будут иметь правильные ID.')

if __name__ == '__main__':
    fix_sequences()
