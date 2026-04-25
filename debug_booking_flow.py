#!/usr/bin/env python
"""
Debug booking flow to find technical messages.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule

def debug_booking_flow():
    """Debug booking flow"""
    print('=== ОТЛАДКА: Процесс бронирования ===')
    print()
    
    # 1. Проверяем API endpoint
    print('1. Проверяем API endpoint /api/temp-booking/:')
    print('   Этот endpoint используется для создания временного бронирования')
    print()
    
    # 2. Проверяем расписание
    schedules = Schedule.objects.all()
    print('2. Доступные расписания для тестирования:')
    for schedule in schedules[:3]:
        print(f'   - ID: {schedule.id}, {schedule.route.departure_city} -> {schedule.route.arrival_city}')
    print()
    
    # 3. Проверяем возможные проблемы
    print('3. Возможные источники технических сообщений:')
    print('   - console.log сообщения в JavaScript')
    print('   - Ошибки API /api/temp-booking/')
    print('   - Проблемы с CSRF токеном')
    print('   - Проблемы с форматом данных')
    print()
    
    # 4. Проверяем view для temp-booking
    print('4. Проверяем view для temp-booking:')
    from tickets.views import create_temp_booking
    print('   View найден: create_temp_booking')
    print()
    
    print('=== РЕКОМЕНДАЦИИ ===')
    print('1. Откройте консоль разработчика (F12)')
    print('2. Выберите места и нажмите Continue to Booking')
    print('3. Посмотрите на сообщения в консоли')
    print('4. Проверьте вкладку Network для запроса /api/temp-booking/')
    print()
    print('Если есть технические сообщения, они будут видны в консоли.')

if __name__ == '__main__':
    debug_booking_flow()
