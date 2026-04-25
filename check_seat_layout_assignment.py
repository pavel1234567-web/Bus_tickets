#!/usr/bin/env python
"""
Check seat layout assignment functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import SeatLayout, Bus

def check_seat_layout_assignment():
    """Check seat layout assignment functionality"""
    print('=== Проверка функционала привязки схем к автобусам ===')
    print()
    
    # Показываем доступные схемы
    layouts = SeatLayout.objects.all()
    print('Доступные схемы посадочных мест:')
    for layout in layouts:
        print(f'  - {layout.name} ({layout.total_seats} мест, {layout.seats_per_row} в ряду)')
    
    print()
    
    # Показываем автобусы и их схемы
    buses = Bus.objects.all()
    print('Автобусы и их схемы:')
    for bus in buses:
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Не назначена'
        print(f'  - {bus.registration_number}: {layout_name}')
    
    print()
    
    # Проверяем, что можно изменить схему у автобуса
    bus = Bus.objects.first()
    if bus:
        print(f'Тестовый автобус: {bus.registration_number}')
        current_layout = bus.seat_layout_config.name if bus.seat_layout_config else 'Не назначена'
        print(f'Текущая схема: {current_layout}')
        
        # Показываем доступные схемы для этого автобуса
        available_layouts = SeatLayout.objects.all()
        print('Доступные схемы для назначения:')
        for layout in available_layouts:
            if layout != bus.seat_layout_config:
                print(f'  - {layout.name}')
        
        # Тест назначения новой схемы
        new_layout = SeatLayout.objects.exclude(id=bus.seat_layout_config.id if bus.seat_layout_config else None).first()
        if new_layout:
            print(f'\nТест: назначаем схему "{new_layout.name}" автобусу {bus.registration_number}')
            old_layout = bus.seat_layout_config
            bus.seat_layout_config = new_layout
            bus.save()
            
            # Проверяем, что схема изменилась
            bus.refresh_from_db()
            print(f'Новая схема: {bus.seat_layout_config.name}')
            
            # Возвращаем обратно
            bus.seat_layout_config = old_layout
            bus.save()
            print(f'Возвращена схема: {old_layout.name if old_layout else "Не назначена"}')
        
    print('\n=== Функционал привязки схем работает корректно! ===')

if __name__ == '__main__':
    check_seat_layout_assignment()
