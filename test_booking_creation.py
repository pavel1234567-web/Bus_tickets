#!/usr/bin/env python
"""
Test booking creation to find ID uniqueness issues.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Schedule, Booking, Ticket
from django.contrib.auth.models import User

def test_booking_creation():
    """Test booking creation process"""
    print('=== ТЕСТИРОВАНИЕ СОЗДАНИЯ БРОНИРОВАНИЯ ===')
    print()
    
    # 1. Проверяем, что есть расписание
    schedules = Schedule.objects.all()
    if not schedules:
        print('Нет расписаний для тестирования')
        return
    
    schedule = schedules.first()
    print(f'Используем расписание: {schedule.route.departure_city} -> {schedule.route.arrival_city}')
    print(f'Автобус: {schedule.bus.registration_number}')
    print()
    
    # 2. Создаем тестового пользователя
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password('test123')
        user.save()
        print('Создан тестовый пользователь: testuser')
    else:
        print('Используем существующий пользователь: testuser')
    
    print()
    
    # 3. Тестируем создание бронирования
    print('3. Тестируем создание бронирования:')
    try:
        # Создаем бронирование
        booking = Booking.objects.create(
            schedule=schedule,
            user=user,
            total_amount=schedule.current_price * 2,  # 2 билета
            status='pending'
        )
        
        print(f'   + Бронирование создано: ID={booking.id}')
        
        # Создаем билеты
        ticket1 = Ticket.objects.create(
            booking=booking,
            seat_number='1A',
            price=schedule.current_price,
            status='booked'
        )
        
        ticket2 = Ticket.objects.create(
            booking=booking,
            seat_number='1B',
            price=schedule.current_price,
            status='booked'
        )
        
        print(f'   + Билеты созданы: ID={ticket1.id}, ID={ticket2.id}')
        
        # Проверяем, что все в порядке
        print(f'   + Все создано успешно!')
        
    except Exception as e:
        print(f'   - Ошибка при создании: {e}')
        import traceback
        traceback.print_exc()
    
    print()
    
    # 4. Проверяем текущее состояние
    print('4. Текущее состояние:')
    print(f'   Бронирований: {Booking.objects.count()}')
    print(f'   Билетов: {Ticket.objects.count()}')
    
    # Показываем последние ID
    if Booking.objects.exists():
        latest_booking = Booking.objects.latest('id')
        print(f'   Последнее бронирование: ID={latest_booking.id}')
    
    if Ticket.objects.exists():
        latest_ticket = Ticket.objects.latest('id')
        print(f'   Последний билет: ID={latest_ticket.id}')
    
    print()
    
    # 5. Проверяем API endpoint
    print('5. Проверяем API endpoint /api/temp-booking/:')
    print('   Этот endpoint используется при нажатии Continue to Booking')
    print('   Нужно проверить, что он работает правильно')
    
    # Удаляем тестовое бронирование
    Booking.objects.filter(user=user).delete()
    print('   Тестовое бронирование удалено')
    
    print()
    print('=== ГОТОВО! ===')

if __name__ == '__main__':
    test_booking_creation()
