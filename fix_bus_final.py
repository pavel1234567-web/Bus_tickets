#!/usr/bin/env python
"""
Final fix for bus seat layouts.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Bus, SeatLayout

def fix_bus_final():
    """Final fix for bus seat layouts"""
    print('=== ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ СХЕМ МЕСТ ===')
    print()
    
    # 1. Получаем все схемы
    layouts = SeatLayout.objects.all()
    layout_dict = {layout.total_seats: layout for layout in layouts}
    
    print('Доступные схемы:')
    for seats, layout in layout_dict.items():
        print(f'  - {layout.name} ({seats} мест)')
    print()
    
    # 2. Исправляем назначения
    buses = Bus.objects.all()
    fixed_count = 0
    
    for bus in buses:
        print(f'Автобус {bus.registration_number} ({bus.total_seats} мест)...')
        
        if bus.total_seats in layout_dict:
            correct_layout = layout_dict[bus.total_seats]
            
            if bus.seat_layout_config != correct_layout:
                print(f'  ИЗМЕНЯЕМ: {bus.seat_layout_config.name if bus.seat_layout_config else "Нет"} -> {correct_layout.name}')
                bus.seat_layout_config = correct_layout
                bus.save()
                fixed_count += 1
            else:
                print(f'  УЖЕ ПРАВИЛЬНО: {correct_layout.name}')
        else:
            # Создаем новую схему
            layout_name = f'{bus.registration_number} Layout ({bus.total_seats} seats)'
            
            if not SeatLayout.objects.filter(name=layout_name).exists():
                new_layout = SeatLayout.objects.create(
                    name=layout_name,
                    description=f'Схема для {bus.registration_number}',
                    total_seats=bus.total_seats,
                    seats_per_row=bus.seats_per_row
                )
                new_layout.layout_data = new_layout.generate_default_layout()
                new_layout.save()
                
                bus.seat_layout_config = new_layout
                bus.save()
                fixed_count += 1
                print(f'  СОЗДАНА новая схема: {layout_name}')
            else:
                existing_layout = SeatLayout.objects.get(name=layout_name)
                bus.seat_layout_config = existing_layout
                bus.save()
                fixed_count += 1
                print(f'  ИСПОЛЬЗОВАНА существующая схема: {layout_name}')
    
    print()
    print(f'ИСПРАВЛЕНО: {fixed_count} автобусов')
    print()
    
    # 3. Проверяем результат
    print('Проверяем результат:')
    for bus in buses:
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        match = '+' if bus.seat_layout_config and bus.total_seats == bus.seat_layout_config.total_seats else '-'
        print(f'  {match} {bus.registration_number}: {bus.total_seats} мест -> {layout_name}')
    
    print()
    print('=== ГОТОВО ДЛЯ ТЕСТИРОВАНИЯ ===')
    print('1. Перезапустите сервер')
    print('2. Очистите кэш браузера')
    print('3. Проверьте админ-панель')
    print('4. Проверьте страницу выбора мест')

if __name__ == '__main__':
    fix_bus_final()
