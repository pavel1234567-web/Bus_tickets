#!/usr/bin/env python
"""
Final test of seat layout functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Bus, SeatLayout

def test_final_functionality():
    """Final comprehensive test"""
    print('=== ФИНАЛЬНЫЙ ТЕСТ: Полный функционал схем мест ===')
    print()
    
    # 1. Проверяем все автобусы и их схемы
    print('1. Проверяем автобусы и схемы:')
    buses = Bus.objects.all()
    for bus in buses:
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        match = '✅' if bus.seat_layout_config and bus.total_seats == bus.seat_layout_config.total_seats else '❌'
        print(f'   {match} {bus.registration_number}: {bus.total_seats} мест -> {layout_name}')
    print()
    
    # 2. Проверяем расписание
    print('2. Проверяем расписание:')
    schedules = Schedule.objects.all()
    for schedule in schedules[:3]:
        bus = schedule.bus
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        match = '✅' if bus.seat_layout_config and bus.total_seats == bus.seat_layout_config.total_seats else '❌'
        print(f'   {match} {schedule.route.departure_city} -> {schedule.route.arrival_city}: {bus.registration_number} ({layout_name})')
    print()
    
    # 3. Тестируем генерацию схемы для фронтенда
    print('3. Тестируем генерацию схемы для фронтенда:')
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
        print(f'   Всего мест в схеме: {sum(1 for row in seat_layout for seat in row if seat)}')
        print(f'   Мест со статусом: {len(seat_status)}')
        
        # Проверяем соответствие
        layout_seats = set()
        for row in seat_layout:
            for seat in row:
                if seat:
                    layout_seats.add(seat['number'])
        
        status_seats = set(seat_status.keys())
        
        if layout_seats == status_seats:
            print('   ✅ Все места соответствуют!')
        else:
            missing = status_seats - layout_seats
            extra = layout_seats - status_seats
            if missing:
                print(f'   ❌ Места нет в схеме: {missing}')
            if extra:
                print(f'   ❌ Лишние места: {extra}')
    else:
        print('   ❌ Нет расписания с назначенной схемой')
    
    print()
    print('=== ИНСТРУКЦИИ ДЛЯ ТЕСТИРОВАНИЯ ===')
    print('1. Откройте: http://127.0.0.1:8000/admin/')
    print('2. Войдите: admin / admin123')
    print('3. Перейдите: Tickets -> Schedules')
    print('4. Выберите любой рейс для просмотра схемы мест')
    print('5. Проверьте, что схема соответствует конфигурации автобуса')
    print()
    print('=== ГОТОВО К ТЕСТИРОВАНИЮ! ===')

if __name__ == '__main__':
    test_final_functionality()
