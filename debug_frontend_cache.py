#!/usr/bin/env python
"""
Debug frontend cache issue with seat layouts.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Bus, SeatLayout
from django.core.cache import cache

def debug_frontend_cache():
    """Debug frontend cache issues"""
    print('=== ОТЛАДКА: Проблема кэширования схем мест ===')
    print()
    
    # 1. Проверяем состояние кэша
    print('1. Проверяем кэш:')
    cache_keys = cache.keys('*')
    print(f'   Ключи в кэше: {len(cache_keys)}')
    for key in cache_keys[:5]:  # Показываем первые 5
        print(f'   - {key}')
    print()
    
    # 2. Проверяем данные в базе
    print('2. Проверяем данные в базе:')
    schedules = Schedule.objects.all()
    for schedule in schedules[:3]:
        bus = schedule.bus
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        print(f'   {schedule.route.departure_city}->{schedule.route.arrival_city}: {bus.registration_number} -> {layout_name}')
        
        # Проверяем, что данные свежие
        layout_data = bus.seat_layout_config.get_layout_display() if bus.seat_layout_config else None
        if layout_data:
            print(f'     Схема в базе: {len(layout_data)} рядов')
        else:
            print('     Схема в базе: None')
    print()
    
    # 3. Очищаем кэш
    print('3. Очищаем кэш:')
    cache.clear()
    print('   + Кэш очищен')
    print()
    
    # 4. Проверяем после очистки
    print('4. Проверяем после очистки кэша:')
    cache_keys_after = cache.keys('*')
    print(f'   Ключей в кэше: {len(cache_keys_after)}')
    print()
    
    # 5. Тестируем прямое получение данных
    print('5. Тестируем прямое получение данных:')
    schedule = schedules.first()
    if schedule:
        bus = schedule.bus
        print(f'   Автобус: {bus.registration_number}')
        print(f'   Схема в базе: {bus.seat_layout_config.name if bus.seat_layout_config else "Нет"}')
        
        # Проверяем метод get_layout_display
        if bus.seat_layout_config:
            layout = bus.seat_layout_config.get_layout_display()
            print(f'   get_layout_display(): {len(layout)} рядов')
            print(f'   Первый ряд: {layout[0] if layout else "Нет"}')
        
        # Проверяем свойство seat_layout (которое использует фронтенд)
        bus_layout = bus.seat_layout
        print(f'   seat_layout свойство: {len(bus_layout)} рядов')
        print(f'   Первый ряд: {bus_layout[0] if bus_layout else "Нет"}')
        
        # Сравниваем
        if bus.seat_layout_config:
            layout_data = bus.seat_layout_config.get_layout_display()
            if layout_data == bus_layout:
                print('   + Данные совпадают!')
            else:
                print('   - Данные НЕ совпадают!')
                print(f'     Схема из модели: {len(layout_data)} рядов')
                print(f'     Свойство seat_layout: {len(bus_layout)} рядов')
    
    print()
    print('=== РЕКОМЕНДАЦИИ ===')
    print('1. Перезапустите сервер разработки')
    print('2. Очистите кэш браузера (Ctrl+F5)')
    print('3. Проверьте настройки кэширования в settings.py')
    print('4. Убедитесь, что нет middleware кэширования')

if __name__ == '__main__':
    debug_frontend_cache()
