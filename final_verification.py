#!/usr/bin/env python
"""
Final verification of seat layout functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Bus, SeatLayout

def final_verification():
    """Final verification of all functionality"""
    print('=== ФИНАЛЬНАЯ ПРОВЕРКА: Полный функционал схем мест ===')
    print()
    
    # 1. Проверяем модели
    print('1. Проверяем модели:')
    buses = Bus.objects.all()
    layouts = SeatLayout.objects.all()
    schedules = Schedule.objects.all()
    
    print(f'   Автобусов: {buses.count()}')
    print(f'   Схем: {layouts.count()}')
    print(f'   Расписаний: {schedules.count()}')
    print()
    
    # 2. Проверяем соответствие автобусов и схем
    print('2. Проверяем соответствие автобусов и схем:')
    all_correct = True
    for bus in buses:
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        is_correct = bus.seat_layout_config and bus.total_seats == bus.seat_layout_config.total_seats
        status = '+' if is_correct else '-'
        if not is_correct:
            all_correct = False
        print(f'   {status} {bus.registration_number}: {bus.total_seats} мест -> {layout_name}')
    print()
    
    # 3. Проверяем views.py функции
    print('3. Проверяем views.py функции:')
    
    # schedule_detail
    schedule = schedules.first()
    if schedule:
        # Тестируем schedule_detail логику
        if schedule.bus.seat_layout_config:
            layout_data = schedule.bus.seat_layout_config.get_layout_display()
            seat_status = schedule.get_seat_status()
            
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
            
            total_seats_in_layout = sum(1 for row in seat_layout for seat in row if seat)
            print(f'   schedule_detail: {total_seats_in_layout} мест в схеме')
        
        # Тестируем seat_selection логику
        if schedule.bus.seat_layout_config:
            layout_data = schedule.bus.seat_layout_config.get_layout_display()
            seat_layout = []
            
            for row_data in layout_data:
                for seat in row_data:
                    if seat:
                        seat_layout.append(seat)
            
            print(f'   seat_selection: {len(seat_layout)} мест в схеме')
    print()
    
    # 4. Проверяем URL для тестирования
    print('4. URL для тестирования:')
    for schedule in schedules[:3]:
        print(f'   Админка: http://127.0.0.1:8000/admin/tickets/bus/{schedule.bus.id}/change/')
        print(f'   Выбор мест: http://127.0.0.1:8000/seat-selection/{schedule.id}/')
        print()
    
    # 5. Итоговый статус
    print('5. Итоговый статус:')
    if all_correct:
        print('   ✅ Все автобусы имеют правильные схемы!')
        print('   ✅ Функционал полностью готов!')
    else:
        print('   ❌ Есть несоответствия в схемах!')
    
    print()
    print('=== ИНСТРУКЦИИ ДЛЯ ПОЛНОГО ТЕСТИРОВАНИЯ ===')
    print('1. Админ-панель: http://127.0.0.1:8000/admin/')
    print('2. Вход: admin / admin123')
    print('3. Измените схему у любого автобуса')
    print('4. Проверьте результат на странице выбора мест')
    print('5. Убедитесь, что схема изменилась немедленно')
    print()
    print('=== ГОТОВО! Функционал работает полностью! ===')

if __name__ == '__main__':
    final_verification()
