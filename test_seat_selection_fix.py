#!/usr/bin/env python
"""
Test seat selection fix.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Bus, SeatLayout

def test_seat_selection_fix():
    """Test seat selection fix"""
    print('=== ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЯ ВЫБОРА МЕСТ ===')
    print()
    
    # 1. Проверяем расписание
    schedules = Schedule.objects.all()
    print(f'Всего расписаний: {schedules.count()}')
    print()
    
    for schedule in schedules[:3]:
        bus = schedule.bus
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        print(f'Расписание {schedule.id}: {schedule.route.departure_city} -> {schedule.route.arrival_city}')
        print(f'  Автобус: {bus.registration_number} ({bus.total_seats} мест)')
        print(f'  Схема: {layout_name}')
        print()
        
        # Тестируем логику из seat_selection
        if bus.seat_layout_config:
            layout_data = bus.seat_layout_config.get_layout_display()
            seat_layout = []
            
            for row_data in layout_data:
                for seat in row_data:
                    if seat:
                        seat_layout.append(seat)
        else:
            seat_layout = []
            for i in range(1, bus.total_seats + 1):
                seat_layout.append(i)
        
        print(f'  Схема для фронтенда: {len(seat_layout)} мест')
        print(f'  Первые 10 мест: {seat_layout[:10]}')
        print()
    
    # 2. Проверяем URL для тестирования
    print('URL для тестирования:')
    for schedule in schedules[:3]:
        print(f'  http://127.0.0.1:8000/seat-selection/{schedule.id}/')
    print()
    
    print('=== ГОТОВО ДЛЯ ТЕСТИРОВАНИЯ ===')
    print('1. Перезапустите сервер')
    print('2. Очистите кэш браузера')
    print('3. Откройте URL выше')
    print('4. Проверьте, что схема соответствует конфигурации автобуса')

if __name__ == '__main__':
    test_seat_selection_fix()
