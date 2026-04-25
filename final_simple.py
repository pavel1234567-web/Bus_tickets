#!/usr/bin/env python
"""
Simple final verification.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Bus, SeatLayout

def final_simple():
    """Simple final verification"""
    print('=== ПРОСТАЯ ФИНАЛЬНАЯ ПРОВЕРКА ===')
    print()
    
    # 1. Проверяем автобусы и схемы
    print('1. Автобусы и схемы:')
    buses = Bus.objects.all()
    for bus in buses:
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        is_correct = bus.seat_layout_config and bus.total_seats == bus.seat_layout_config.total_seats
        status = '+' if is_correct else '-'
        print(f'   {status} {bus.registration_number}: {bus.total_seats} мест -> {layout_name}')
    print()
    
    # 2. Проверяем URL
    print('2. URL для тестирования:')
    schedules = Schedule.objects.all()
    for schedule in schedules[:3]:
        print(f'   Выбор мест: http://127.0.0.1:8000/seat-selection/{schedule.id}/')
        print(f'   Админка: http://127.0.0.1:8000/admin/tickets/bus/{schedule.bus.id}/change/')
    print()
    
    # 3. Проверяем views.py
    print('3. Проверяем views.py:')
    schedule = schedules.first()
    if schedule:
        # schedule_detail
        if schedule.bus.seat_layout_config:
            layout_data = schedule.bus.seat_layout_config.get_layout_display()
            print(f'   schedule_detail: {len(layout_data)} рядов')
        
        # seat_selection  
        if schedule.bus.seat_layout_config:
            layout_data = schedule.bus.seat_layout_config.get_layout_display()
            seat_layout = []
            for row_data in layout_data:
                for seat in row_data:
                    if seat:
                        seat_layout.append(seat)
            print(f'   seat_selection: {len(seat_layout)} мест')
    print()
    
    print('=== ГОТОВО! ===')
    print('1. Перезапустите сервер')
    print('2. Очистите кэш браузера')
    print('3. Проверьте админку и выбор мест')
    print('4. Схемы должны соответствовать!')

if __name__ == '__main__':
    final_simple()
