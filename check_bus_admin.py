#!/usr/bin/env python
"""
Check bus admin functionality and seat layout field.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Bus, SeatLayout
from django.db import models

def check_bus_admin():
    """Check bus admin functionality"""
    print('=== Проверка админ-панели автобусов ===')
    print()
    
    # Проверяем модели
    print('1. Проверка модели Bus:')
    try:
        bus_fields = [f.name for f in Bus._meta.fields]
        print(f'   Поля модели: {bus_fields}')
        
        if 'seat_layout_config' in bus_fields:
            print('   + Поле seat_layout_config существует в модели')
        else:
            print('   - Поле seat_layout_config НЕ существует в модели')
            
    except Exception as e:
        print(f'   - Ошибка при проверке модели: {e}')
    
    print()
    
    # Проверяем существующие автобусы
    print('2. Проверка существующих автобусов:')
    try:
        buses = Bus.objects.all()
        print(f'   Всего автобусов: {buses.count()}')
        
        for bus in buses:
            print(f'   - {bus.registration_number}')
            print(f'     seat_layout_config: {bus.seat_layout_config}')
            print(f'     has attr: {hasattr(bus, "seat_layout_config")}')
            
    except Exception as e:
        print(f'   - Ошибка при проверке автобусов: {e}')
    
    print()
    
    # Проверяем доступные схемы
    print('3. Проверка доступных схем:')
    try:
        layouts = SeatLayout.objects.all()
        print(f'   Всего схем: {layouts.count()}')
        
        for layout in layouts:
            print(f'   - {layout.name} (ID: {layout.id})')
            
    except Exception as e:
        print(f'   - Ошибка при проверке схем: {e}')
    
    print()
    
    # Проверяем связь
    print('4. Проверка связи между моделями:')
    try:
        bus = Bus.objects.first()
        if bus:
            print(f'   Тестовый автобус: {bus.registration_number}')
            
            # Проверяем, можно ли назначить схему
            layout = SeatLayout.objects.first()
            if layout:
                print(f'   Тестовая схема: {layout.name}')
                
                # Пробуем назначить
                old_layout = bus.seat_layout_config
                bus.seat_layout_config = layout
                bus.save()
                
                # Проверяем, что сохранилось
                bus.refresh_from_db()
                print(f'   Назначена схема: {bus.seat_layout_config.name if bus.seat_layout_config else "None"}')
                
                # Возвращаем обратно
                bus.seat_layout_config = old_layout
                bus.save()
                print('   + Связь работает корректно')
            else:
                print('   - Нет доступных схем')
        else:
            print('   - Нет автобусов для тестирования')
            
    except Exception as e:
        print(f'   - Ошибка при проверке связи: {e}')

if __name__ == '__main__':
    check_bus_admin()
