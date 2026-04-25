#!/usr/bin/env python
"""
Fix seat layout mismatch between buses and layouts.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Bus, SeatLayout

def fix_seat_layout_mismatch():
    """Fix seat layout mismatch"""
    print('=== Исправление несоответствия схем мест ===')
    print()
    
    buses = Bus.objects.all()
    layouts = SeatLayout.objects.all()
    
    print('Проверяем соответствие автобусов и схем:')
    for bus in buses:
        print(f'Автобус {bus.registration_number}:')
        print(f'  Мест в автобусе: {bus.total_seats}')
        print(f'  Мест в ряду: {bus.seats_per_row}')
        
        if bus.seat_layout_config:
            print(f'  Текущая схема: {bus.seat_layout_config.name}')
            print(f'  Мест в схеме: {bus.seat_layout_config.total_seats}')
            print(f'  Мест в ряду в схеме: {bus.seat_layout_config.seats_per_row}')
            
            if bus.total_seats != bus.seat_layout_config.total_seats:
                print(f'  ! НЕСООТВЕТСТВИЕ: {bus.total_seats} != {bus.seat_layout_config.total_seats}')
                
                # Ищем подходящую схему
                suitable_layout = None
                for layout in layouts:
                    if layout.total_seats == bus.total_seats:
                        suitable_layout = layout
                        break
                
                if suitable_layout:
                    print(f'  + Найдена подходящая схема: {suitable_layout.name}')
                    bus.seat_layout_config = suitable_layout
                    bus.save()
                    print(f'  + Схема изменена на: {suitable_layout.name}')
                else:
                    print(f'  - Не найдено подходящей схемы для {bus.total_seats} мест')
                    
                    # Создаем новую схему для этого автобуса
                    layout_name = f'Custom {bus.total_seats} seats'
                    if not SeatLayout.objects.filter(name=layout_name).exists():
                        new_layout = SeatLayout.objects.create(
                            name=layout_name,
                            description=f'Автоматически созданная схема для {bus.total_seats} мест',
                            total_seats=bus.total_seats,
                            seats_per_row=bus.seats_per_row
                        )
                        new_layout.layout_data = new_layout.generate_default_layout()
                        new_layout.save()
                        
                        bus.seat_layout_config = new_layout
                        bus.save()
                        print(f'  + Создана новая схема: {layout_name}')
            else:
                print(f'  ✅ Соответствие: {bus.total_seats} == {bus.seat_layout_config.total_seats}')
        else:
            print(f'  - Нет назначенной схемы')
        print()
    
    print('Проверяем результат:')
    for bus in buses:
        if bus.seat_layout_config:
            match = bus.total_seats == bus.seat_layout_config.total_seats
            status = '+' if match else '-'
            print(f'{status} {bus.registration_number}: {bus.total_seats} мест -> {bus.seat_layout_config.name} ({bus.seat_layout_config.total_seats} мест)')

if __name__ == '__main__':
    fix_seat_layout_mismatch()
