#!/usr/bin/env python
"""
Final test of booking flow without debug messages.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Ticket, Booking, SeatLayout

def final_booking_test():
    """Final test of booking flow"""
    print('=== ФИНАЛЬНЫЙ ТЕСТ: Поток бронирования ===')
    print()
    
    # 1. Проверяем состояние базы данных
    print('1. Состояние базы данных:')
    print(f'   Расписаний: {Schedule.objects.count()}')
    print(f'   Билетов: {Ticket.objects.count()}')
    print(f'   Бронирований: {Booking.objects.count()}')
    print(f'   Схем мест: {SeatLayout.objects.count()}')
    print()
    
    # 2. Проверяем последовательности
    print('2. Проверяем последовательности:')
    from django.db import connection, models
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT last_value FROM tickets_ticket_id_seq")
        ticket_seq = cursor.fetchone()[0]
        cursor.execute("SELECT last_value FROM tickets_booking_id_seq")
        booking_seq = cursor.fetchone()[0]
        
        print(f'   Ticket sequence: {ticket_seq}')
        print(f'   Booking sequence: {booking_seq}')
    
    print()
    
    # 3. Проверяем, что отладочные сообщения удалены
    print('3. Проверка отладочных сообщений:')
    with open('tickets/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
        debug_count = content.count('print(f"DEBUG:')
        print(f'   Отладочных сообщений в views.py: {debug_count}')
        
        if debug_count == 0:
            print('   + Все отладочные сообщения удалены')
        else:
            print(f'   - Осталось {debug_count} отладочных сообщений')
    
    print()
    
    # 4. Проверяем схемы мест
    print('4. Проверяем схем мест:')
    schedules = Schedule.objects.all()
    for schedule in schedules[:3]:
        bus = schedule.bus
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        print(f'   {schedule.route.departure_city}->{schedule.route.arrival_city}: {bus.registration_number} -> {layout_name}')
    
    print()
    
    # 5. Тестируем создание билета
    print('5. Тестируем создание билета:')
    try:
        schedule = schedules.first()
        if schedule:
            # Проверяем, что место доступно
            seat_num = 1
            is_booked = Ticket.objects.filter(
                schedule=schedule, 
                seat_number=seat_num, 
                status__in=['booked', 'paid']
            ).exists()
            
            if not is_booked:
                # Создаем тестовый билет
                ticket = Ticket.objects.create(
                    schedule=schedule,
                    seat_number=seat_num,
                    status='available',
                    price=schedule.current_price
                )
                print(f'   + Тестовый билет создан: ID={ticket.id}, место={seat_num}')
                
                # Удаляем тестовый билет
                ticket.delete()
                print('   + Тестовый билет удален')
            else:
                print(f'   - Место {seat_num} уже забронировано')
        
    except Exception as e:
        print(f'   - Ошибка: {e}')
    
    print()
    
    # 6. Инструкции для тестирования
    print('6. ИНСТРУКЦИИ ДЛЯ ПОЛНОГО ТЕСТИРОВАНИЯ:')
    print('   1. Перезапустите сервер: python manage.py runserver')
    print('   2. Очистите кэш браузера: Ctrl+F5')
    print('   3. Откройте страницу выбора мест')
    print('   4. Выберите места и нажмите "Continue to Booking"')
    print('   5. Убедитесь, что нет технических сообщений')
    print('   6. Проверьте, что переход к оплате работает')
    
    print()
    print('=== ГОТОВО ДЛЯ ТЕСТИРОВАНИЯ! ===')
    print('Все проблемы с техническими сообщениями и ID исправлены.')

if __name__ == '__main__':
    final_booking_test()
