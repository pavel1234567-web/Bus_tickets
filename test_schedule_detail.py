#!/usr/bin/env python
"""
Test schedule detail view with new seat layout functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Bus, SeatLayout

def test_schedule_detail():
    """Test schedule detail view functionality"""
    print('=== Тестирование schedule_detail с новыми схемами ===')
    print()
    
    # Находим расписание с автобусом, у которого есть схема
    schedules = Schedule.objects.all()
    schedule_with_layout = None
    
    for schedule in schedules:
        if schedule.bus.seat_layout_config:
            schedule_with_layout = schedule
            break
    
    if schedule_with_layout:
        print(f'Расписание: {schedule_with_layout}')
        print(f'Автобус: {schedule_with_layout.bus.registration_number}')
        print(f'Схема: {schedule_with_layout.bus.seat_layout_config.name}')
        print()
        
        # Получаем статус мест
        seat_status = schedule_with_layout.get_seat_status()
        print(f'Статус мест: {len(seat_status)} мест')
        
        # Получаем схему из модели
        layout_data = schedule_with_layout.bus.seat_layout_config.get_layout_display()
        print(f'Схема из модели: {len(layout_data)} рядов')
        
        # Показываем первые несколько рядов
        for i, row in enumerate(layout_data[:3]):
            print(f'  Ряд {i+1}: {row}')
        
        # Проверяем, что места из схемы соответствуют статусу
        total_seats_in_layout = sum(1 for row in layout_data for seat in row if seat)
        print(f'Всего мест в схеме: {total_seats_in_layout}')
        print(f'Мест со статусом: {len(seat_status)}')
        
        if total_seats_in_layout == len(seat_status):
            print('+ Количество мест совпадает!')
        else:
            print('- Количество мест НЕ совпадает!')
            
        # Проверяем, что все места из схемы есть в статусе
        layout_seats = set()
        for row in layout_data:
            for seat in row:
                if seat:
                    layout_seats.add(seat)
        
        status_seats = set(seat_status.keys())
        
        if layout_seats == status_seats:
            print('+ Наборы мест совпадают!')
        else:
            print('- Наборы мест НЕ совпадают!')
            missing_in_status = layout_seats - status_seats
            missing_in_layout = status_seats - layout_seats
            if missing_in_status:
                print(f'  Места нет в статусе: {missing_in_status}')
            if missing_in_layout:
                print(f'  Места нет в схеме: {missing_in_layout}')
        
    else:
        print('Нет расписаний с назначенными схемами!')
        print('Доступные расписания:')
        for schedule in schedules[:3]:
            print(f'  - {schedule} (автобус: {schedule.bus.registration_number})')

if __name__ == '__main__':
    test_schedule_detail()
