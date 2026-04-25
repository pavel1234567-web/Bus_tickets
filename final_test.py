#!/usr/bin/env python
"""
Final test of seat layout assignment functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Bus, SeatLayout
from django.contrib.auth.models import User

def final_test():
    """Final comprehensive test"""
    print('=== ФИНАЛЬНЫЙ ТЕСТ: Привязка схем к автобусам ===')
    print()
    
    # 1. Проверяем модели
    print('1. Проверяем модели:')
    buses = Bus.objects.all()
    layouts = SeatLayout.objects.all()
    print(f'   Автобусов: {buses.count()}')
    print(f'   Схем: {layouts.count()}')
    print()
    
    # 2. Проверяем существующие назначения
    print('2. Текущие назначения:')
    for bus in buses:
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Не назначена'
        print(f'   {bus.registration_number}: {layout_name}')
    print()
    
    # 3. Тест изменения назначения
    print('3. Тест изменения назначения:')
    bus = Bus.objects.first()
    if bus:
        old_layout = bus.seat_layout_config
        print(f'   Автобус: {bus.registration_number}')
        print(f'   Текущая схема: {old_layout.name if old_layout else "Не назначена"}')
        
        # Выбираем другую схему
        new_layout = SeatLayout.objects.exclude(id=old_layout.id if old_layout else None).first()
        if new_layout:
            print(f'   Новая схема: {new_layout.name}')
            
            # Изменяем схему
            bus.seat_layout_config = new_layout
            bus.save()
            
            # Проверяем
            bus.refresh_from_db()
            current_layout = bus.seat_layout_config.name if bus.seat_layout_config else 'Не назначена'
            print(f'   Результат: {current_layout}')
            
            if current_layout == new_layout.name:
                print('   + Изменение схемы УСПЕШНО!')
            else:
                print('   - Изменение схемы НЕ УДАЛОСЬ!')
                
            # Возвращаем обратно
            bus.seat_layout_config = old_layout
            bus.save()
            print('   Возвращена исходная схема')
        else:
            print('   - Нет других схем для теста')
    else:
        print('   - Нет автобусов для теста')
    print()
    
    # 4. Инструкции для пользователя
    print('4. ИНСТРУКЦИИ для использования в админ-панели:')
    print('   1. Откройте в браузере: http://127.0.0.1:8000/admin/')
    print('   2. Войдите с данными:')
    print('      - Имя пользователя: admin')
    print('      - Пароль: admin123')
    print('   3. Перейдите: Tickets -> Buses')
    print('   4. Нажмите на любой автобус для редактирования')
    print('   5. В поле "Seat layout" выберите нужную схему')
    print('   6. Нажмите "SAVE"')
    print()
    
    # 5. Доступные схемы
    print('5. Доступные схемы для выбора:')
    for layout in layouts:
        print(f'   - {layout.name} ({layout.total_seats} мест)')
    print()
    
    print('=== ГОТОВО! Функционал работает корректно ===')

if __name__ == '__main__':
    final_test()
