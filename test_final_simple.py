#!/usr/bin/env python
"""
Simple final test of seat layout functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Bus, SeatLayout

def test_final_simple():
    """Simple final test"""
    print('=== ПРОСТОЙ ТЕСТ: Схемы мест ===')
    print()
    
    # 1. Проверяем автобусы
    print('1. Автобусы и их схемы:')
    buses = Bus.objects.all()
    for bus in buses:
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        match = '+' if bus.seat_layout_config and bus.total_seats == bus.seat_layout_config.total_seats else '-'
        print(f'   {match} {bus.registration_number}: {bus.total_seats} мест -> {layout_name}')
    print()
    
    # 2. Проверяем расписание
    print('2. Расписания:')
    schedules = Schedule.objects.all()
    for schedule in schedules[:3]:
        bus = schedule.bus
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        match = '+' if bus.seat_layout_config and bus.total_seats == bus.seat_layout_config.total_seats else '-'
        print(f'   {match} {schedule.route.departure_city} -> {schedule.route.arrival_city}: {bus.registration_number} ({layout_name})')
    print()
    
    # 3. Тестируем views.py логику
    print('3. Тест логики из views.py:')
    schedule = schedules.first()
    if schedule and schedule.bus.seat_layout_config:
        # Получаем данные как в views.py
        seat_status = schedule.get_seat_status()
        layout_data = schedule.bus.seat_layout_config.get_layout_display()
        
        # Генерируем seat_layout как в views.py
        seat_layout = []
        for row_data in layout_data:
            row = []
            for seat in row_data:
                if seat and seat in seat_status:
                    row.append({
                        'number': seat,
                        'status': seat_status[seat]
                    })
                elif seat:
                    row.append({
                        'number': seat,
                        'status': 'available'
                    })
                else:
                    row.append(None)
            seat_layout.append(row)
        
        print(f'   Схема сгенерирована: {len(seat_layout)} рядов')
        total_seats_in_layout = sum(1 for row in seat_layout for seat in row if seat)
        total_seats_in_status = len(seat_status)
        
        if total_seats_in_layout == total_seats_in_status:
            print('   + Все места соответствуют!')
        else:
            print(f'   - Несоответствие: {total_seats_in_layout} != {total_seats_in_status}')
    
    print()
    print('=== ИНСТРУКЦИИ ===')
    print('1. Админ-панель: http://127.0.0.1:8000/admin/')
    print('2. Вход: admin / admin123')
    print('3. Выберите автобус и измените схему')
    print('4. Проверьте результат на странице выбора мест')
    print()
    print('=== ГОТОВО! ===')

if __name__ == '__main__':
    test_final_simple()
