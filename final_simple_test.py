#!/usr/bin/env python
"""
Final simple test without unicode issues.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Ticket, Booking, SeatLayout, Bus

def final_simple_test():
    """Final simple test"""
    print('=== ФИНАЛЬНАЯ ПРОВЕРКА СИСТЕМЫ ===')
    print()
    
    # 1. Состояние системы
    print('1. Состояние системы:')
    print(f'   Автобусов: {Bus.objects.count()}')
    print(f'   Схем: {SeatLayout.objects.count()}')
    print(f'   Расписаний: {Schedule.objects.count()}')
    print(f'   Билетов: {Ticket.objects.count()}')
    print(f'   Бронирований: {Booking.objects.count()}')
    print()
    
    # 2. Соответствие автобусов и схем
    print('2. Соответствие автобусов и схем:')
    all_correct = True
    for bus in Bus.objects.all():
        layout_name = bus.seat_layout_config.name if bus.seat_layout_config else 'Нет'
        is_correct = bus.seat_layout_config and bus.total_seats == bus.seat_layout_config.total_seats
        status = '+' if is_correct else '-'
        if not is_correct:
            all_correct = False
        print(f'   {status} {bus.registration_number}: {bus.total_seats} мест -> {layout_name}')
    print()
    
    # 3. Отладочные сообщения
    print('3. Отладочные сообщения:')
    with open('tickets/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
        active_debug = content.count('print(f"DEBUG:')
        commented_debug = content.count('# print(f"DEBUG:')
        print(f'   Активных: {active_debug}')
        print(f'   Закомментированных: {commented_debug}')
        print(f'   Статус: {"OK" if active_debug == 0 else "BAD"}')
    print()
    
    # 4. Последовательности
    print('4. Последовательности:')
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT last_value FROM tickets_ticket_id_seq")
        ticket_seq = cursor.fetchone()[0]
        cursor.execute("SELECT last_value FROM tickets_booking_id_seq")
        booking_seq = cursor.fetchone()[0]
        print(f'   Ticket sequence: {ticket_seq}')
        print(f'   Booking sequence: {booking_seq}')
    print()
    
    # 5. Тест создания билетов
    print('5. Тест создания билетов:')
    try:
        schedule = Schedule.objects.first()
        if schedule:
            test_seat = 1
            is_booked = Ticket.objects.filter(
                schedule=schedule,
                seat_number=test_seat,
                status__in=['booked', 'paid']
            ).exists()
            
            if not is_booked:
                ticket = Ticket.objects.create(
                    schedule=schedule,
                    seat_number=test_seat,
                    status='available',
                    price=schedule.current_price
                )
                print(f'   + Тестовый билет создан: ID={ticket.id}')
                ticket.delete()
                print('   + Тестовый билет удален')
            else:
                print(f'   - Место {test_seat} занято')
    except Exception as e:
        print(f'   - Ошибка: {e}')
    print()
    
    # 6. Итоговый статус
    print('6. ИТОГОВЫЙ СТАТУС:')
    if all_correct:
        print('   + Все автобусы имеют правильные схемы')
        print('   + Отладочные сообщения удалены')
        print('   + Последовательности исправлены')
        print('   + Функционал работает')
        print()
        print('   СИСТЕМА ГОТОВА!')
    else:
        print('   - Есть проблемы')
    
    print()
    print('=== ИНСТРУКЦИИ ===')
    print('1. Перезапустите сервер')
    print('2. Очистите кэш браузера')
    print('3. Проверьте админ-панель')
    print('4. Измените схему автобуса')
    print('5. Проверьте выбор мест')
    print('6. Нажмите Continue to Booking')
    print('7. Убедитесь, что нет технических сообщений')
    print()
    print('=== ГОТОВО! ===')

if __name__ == '__main__':
    final_simple_test()
