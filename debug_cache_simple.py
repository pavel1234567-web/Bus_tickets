#!/usr/bin/env python
"""
Simple cache debug.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.cache import cache
from tickets.models import Schedule, Bus, SeatLayout

def debug_cache_simple():
    """Simple cache debug"""
    print('=== ПРОСТАЯ ОТЛАДКА КЭША ===')
    print()
    
    # 1. Проверяем тип кэша
    print(f'1. Тип кэша: {type(cache)}')
    print()
    
    # 2. Очищаем кэш
    print('2. Очищаем кэш...')
    cache.clear()
    print('   + Кэш очищен')
    print()
    
    # 3. Проверяем данные
    print('3. Проверяем данные:')
    schedules = Schedule.objects.all()
    for schedule in schedules[:3]:
        bus = schedule.bus
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        print(f'   {schedule.route.departure_city}->{schedule.route.arrival_city}: {bus.registration_number} -> {layout_name}')
    print()
    
    # 4. Тестируем прямое получение схемы
    print('4. Тестируем получение схемы:')
    if schedules:
        schedule = schedules.first()
        bus = schedule.bus
        if bus.seat_layout_config:
            # Метод из модели
            layout_model = bus.seat_layout_config.get_layout_display()
            print(f'   get_layout_display(): {len(layout_model)} рядов')
            
            # Свойство (которое использует фронтенд)
            layout_property = bus.seat_layout
            print(f'   seat_layout свойство: {len(layout_property)} рядов')
            
            # Сравниваем
            if layout_model == layout_property:
                print('   + Данные совпадают!')
            else:
                print('   - Данные НЕ совпадают!')
                print(f'     Модель: {len(layout_model)}')
                print(f'     Свойство: {len(layout_property)}')
    print()
    
    # 5. Проверяем настройки
    print('5. Проверяем настройки кэша в settings.py:')
    from django.conf import settings
    if hasattr(settings, 'CACHES'):
        caches = settings.CACHES
        for cache_name, cache_config in caches.items():
            print(f'   {cache_name}: {cache_config}')
    else:
        print('   Настройки CACHES не найдены')
    
    print()
    print('=== РЕКОМЕНДАЦИИ ===')
    print('1. Перезапустите сервер: python manage.py runserver')
    print('2. Очистите кэш браузера: Ctrl+F5')
    print('3. Проверьте, что нет кэширующего middleware')

if __name__ == '__main__':
    debug_cache_simple()
