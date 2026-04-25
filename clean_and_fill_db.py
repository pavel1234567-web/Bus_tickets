#!/usr/bin/env python3
"""
Скрипт для очистки базы данных от некорректных записей и заполнения правильными данными
"""

import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent))

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.db import connection
from tickets.models import Route, Bus, Schedule, Booking, Ticket, Payment
from datetime import datetime, timedelta
from django.utils import timezone

def clean_and_fill_database():
    """Полная очистка и заполнение базы данных правильными данными"""
    print("Очистка и заполнение базы данных...")
    
    # Очистка таблиц
    with connection.cursor() as cursor:
        cursor.execute("SET session_replication_role = replica;")
        cursor.execute("TRUNCATE TABLE tickets_payment RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE tickets_ticket RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE tickets_booking RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE tickets_schedule RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE tickets_bus RESTART IDENTITY CASCADE;")
        cursor.execute("TRUNCATE TABLE tickets_route RESTART IDENTITY CASCADE;")
        cursor.execute("SET session_replication_role = DEFAULT;")
        
        # Сброс счетчиков
        cursor.execute("ALTER SEQUENCE tickets_payment_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE tickets_ticket_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE tickets_booking_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE tickets_schedule_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE tickets_bus_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE tickets_route_id_seq RESTART WITH 1;")
    
    print("Таблицы очищены")
    
    # Получаем текущую дату
    today = timezone.now().date()
    
    # Создание маршрутов с правильными данными
    routes_data = [
        {
            'name': 'Москва - Санкт-Петербург',
            'departure_city': 'Москва',
            'arrival_city': 'Санкт-Петербург',
            'distance': 704.00,
            'estimated_time': timedelta(hours=8),
            'base_price': 2500.00,
            'departure_address': 'Казанский вокзал, Комсомольская площадь, 1',
            'arrival_address': 'Московский вокзал, Невский проспект, 85',
            'departure_date': today + timedelta(days=1)
        },
        {
            'name': 'Москва - Нижний Новгород',
            'departure_city': 'Москва',
            'arrival_city': 'Нижний Новгород',
            'distance': 440.00,
            'estimated_time': timedelta(hours=4, minutes=30),
            'base_price': 1800.00,
            'departure_address': 'Казанский вокзал, Комсомольская площадь, 1',
            'arrival_address': 'Московский вокзал, площадь Горького, 1',
            'departure_date': today
        },
        {
            'name': 'Москва - Казань',
            'departure_city': 'Москва',
            'arrival_city': 'Казань',
            'distance': 819.00,
            'estimated_time': timedelta(hours=12),
            'base_price': 2800.00,
            'departure_address': 'Казанский вокзал, Комсомольская площадь, 1',
            'arrival_address': 'Казанский вокзал, улица Девятаева, 1',
            'departure_date': today + timedelta(days=2)
        },
        {
            'name': 'Санкт-Петербург - Нижний Новгород',
            'departure_city': 'Санкт-Петербург',
            'arrival_city': 'Нижний Новгород',
            'distance': 860.00,
            'estimated_time': timedelta(hours=14),
            'base_price': 3200.00,
            'departure_address': 'Московский вокзал, Невский проспект, 85',
            'arrival_address': 'Московский вокзал, площадь Горького, 1',
            'departure_date': today + timedelta(days=1)
        },
        {
            'name': 'Москва - Екатеринбург',
            'departure_city': 'Москва',
            'arrival_city': 'Екатеринбург',
            'distance': 1778.00,
            'estimated_time': timedelta(hours=24),
            'base_price': 4500.00,
            'departure_address': 'Казанский вокзал, Комсомольская площадь, 1',
            'arrival_address': 'Екатеринбургский вокзал, улица Чайковского, 1',
            'departure_date': today + timedelta(days=3)
        },
        {
            'name': 'Санкт-Петербург - Казань',
            'departure_city': 'Санкт-Петербург',
            'arrival_city': 'Казань',
            'distance': 1500.00,
            'estimated_time': timedelta(hours=18),
            'base_price': 3800.00,
            'departure_address': 'Московский вокзал, Невский проспект, 85',
            'arrival_address': 'Казанский вокзал, улица Девятаева, 1',
            'departure_date': today + timedelta(days=2)
        },
        {
            'name': 'Нижний Новгород - Казань',
            'departure_city': 'Нижний Новгород',
            'arrival_city': 'Казань',
            'distance': 380.00,
            'estimated_time': timedelta(hours=6),
            'base_price': 1500.00,
            'departure_address': 'Московский вокзал, площадь Горького, 1',
            'arrival_address': 'Казанский вокзал, улица Девятаева, 1',
            'departure_date': today + timedelta(days=1)
        },
        {
            'name': 'Москва - Сочи',
            'departure_city': 'Москва',
            'arrival_city': 'Сочи',
            'distance': 1673.00,
            'estimated_time': timedelta(hours=24),
            'base_price': 5500.00,
            'departure_address': 'Казанский вокзал, Комсомольская площадь, 1',
            'arrival_address': 'Сочинский вокзал, улица Горького, 1',
            'departure_date': today + timedelta(days=4)
        }
    ]
    
    routes = []
    for route_data in routes_data:
        route = Route.objects.create(**route_data)
        routes.append(route)
    
    print(f"Создано {len(routes)} маршрутов")
    
    # Создание автобусов
    buses_data = [
        {'registration_number': 'BUS001', 'bus_type': 'standard', 'total_seats': 50, 'seats_per_row': 4, 'has_ac': True, 'has_wifi': False},
        {'registration_number': 'BUS002', 'bus_type': 'standard', 'total_seats': 45, 'seats_per_row': 4, 'has_ac': True, 'has_wifi': True},
        {'registration_number': 'BUS003', 'bus_type': 'comfort', 'total_seats': 36, 'seats_per_row': 4, 'has_ac': True, 'has_wifi': True},
        {'registration_number': 'BUS004', 'bus_type': 'comfort', 'total_seats': 40, 'seats_per_row': 4, 'has_ac': True, 'has_wifi': True},
        {'registration_number': 'BUS005', 'bus_type': 'luxury', 'total_seats': 28, 'seats_per_row': 4, 'has_ac': True, 'has_wifi': True, 'has_toilet': True},
        {'registration_number': 'BUS006', 'bus_type': 'luxury', 'total_seats': 24, 'seats_per_row': 4, 'has_ac': True, 'has_wifi': True, 'has_toilet': True},
    ]
    
    buses = []
    for bus_data in buses_data:
        bus = Bus.objects.create(**bus_data)
        buses.append(bus)
    
    print(f"Создано {len(buses)} автобусов")
    
    # Создание расписаний
    now = timezone.now()
    schedules_data = [
        # Москва - Нижний Новгород (сегодня)
        {'route': routes[1], 'bus': buses[0], 'departure_time': now + timedelta(hours=8), 'arrival_time': now + timedelta(hours=12, minutes=30), 'price_multiplier': 1.0},
        {'route': routes[1], 'bus': buses[1], 'departure_time': now + timedelta(hours=10), 'arrival_time': now + timedelta(hours=14, minutes=30), 'price_multiplier': 1.0},
        {'route': routes[1], 'bus': buses[2], 'departure_time': now + timedelta(hours=14), 'arrival_time': now + timedelta(hours=18, minutes=30), 'price_multiplier': 1.1},
        {'route': routes[1], 'bus': buses[3], 'departure_time': now + timedelta(hours=16), 'arrival_time': now + timedelta(hours=20, minutes=30), 'price_multiplier': 1.0},
        {'route': routes[1], 'bus': buses[0], 'departure_time': now + timedelta(hours=18), 'arrival_time': now + timedelta(hours=22, minutes=30), 'price_multiplier': 1.0},
        
        # Москва - Санкт-Петербург (завтра)
        {'route': routes[0], 'bus': buses[2], 'departure_time': now + timedelta(days=1, hours=7), 'arrival_time': now + timedelta(days=1, hours=15), 'price_multiplier': 1.1},
        {'route': routes[0], 'bus': buses[3], 'departure_time': now + timedelta(days=1, hours=9), 'arrival_time': now + timedelta(days=1, hours=17), 'price_multiplier': 1.0},
        {'route': routes[0], 'bus': buses[4], 'departure_time': now + timedelta(days=1, hours=11), 'arrival_time': now + timedelta(days=1, hours=19), 'price_multiplier': 1.2},
        
        # Москва - Казань (через 2 дня)
        {'route': routes[2], 'bus': buses[4], 'departure_time': now + timedelta(days=2, hours=8), 'arrival_time': now + timedelta(days=2, hours=20), 'price_multiplier': 1.2},
        {'route': routes[2], 'bus': buses[5], 'departure_time': now + timedelta(days=2, hours=10), 'arrival_time': now + timedelta(days=2, hours=22), 'price_multiplier': 1.2},
        
        # Санкт-Петербург - Нижний Новгород (завтра)
        {'route': routes[3], 'bus': buses[2], 'departure_time': now + timedelta(days=1, hours=8), 'arrival_time': now + timedelta(days=1, hours=22), 'price_multiplier': 1.1},
        {'route': routes[3], 'bus': buses[3], 'departure_time': now + timedelta(days=1, hours=10), 'arrival_time': now + timedelta(days=2, hours=0), 'price_multiplier': 1.0},
        
        # Нижний Новгород - Казань (завтра)
        {'route': routes[6], 'bus': buses[1], 'departure_time': now + timedelta(days=1, hours=9), 'arrival_time': now + timedelta(days=1, hours=15), 'price_multiplier': 1.0},
        {'route': routes[6], 'bus': buses[2], 'departure_time': now + timedelta(days=1, hours=13), 'arrival_time': now + timedelta(days=1, hours=19), 'price_multiplier': 1.1},
        
        # Москва - Екатеринбург (через 3 дня)
        {'route': routes[4], 'bus': buses[4], 'departure_time': now + timedelta(days=3, hours=6), 'arrival_time': now + timedelta(days=4, hours=6), 'price_multiplier': 1.3},
        
        # Санкт-Петербург - Казань (через 2 дня)
        {'route': routes[5], 'bus': buses[3], 'departure_time': now + timedelta(days=2, hours=9), 'arrival_time': now + timedelta(days=3, hours=3), 'price_multiplier': 1.2},
        
        # Москва - Сочи (через 4 дня)
        {'route': routes[7], 'bus': buses[5], 'departure_time': now + timedelta(days=4, hours=7), 'arrival_time': now + timedelta(days=5, hours=7), 'price_multiplier': 1.4},
    ]
    
    schedules = []
    for schedule_data in schedules_data:
        schedule = Schedule.objects.create(**schedule_data)
        schedules.append(schedule)
    
    print(f"Создано {len(schedules)} расписаний")
    
    # Создание тестовых бронирований
    bookings_data = [
        {'first_name': 'Иван', 'last_name': 'Петров', 'email': 'ivan.petrov@example.com', 'phone': '+7(900)123-45-67', 'total_price': 1800.00, 'is_paid': False},
        {'first_name': 'Мария', 'last_name': 'Сидорова', 'email': 'maria.sidorova@example.com', 'phone': '+7(900)234-56-78', 'total_price': 2500.00, 'is_paid': True},
        {'first_name': 'Алексей', 'last_name': 'Козлов', 'email': 'alex.kozlov@example.com', 'phone': '+7(900)345-67-89', 'total_price': 3200.00, 'is_paid': False},
    ]
    
    bookings = []
    for booking_data in bookings_data:
        booking = Booking.objects.create(**booking_data)
        bookings.append(bookings)
    
    print(f"Создано {len(bookings)} бронирований")
    
    # Создание билетов
    tickets_data = [
        {'booking': bookings[0], 'schedule': schedules[0], 'seat_number': 15, 'status': 'booked', 'price': 1800.00},
        {'booking': bookings[1], 'schedule': schedules[5], 'seat_number': 12, 'status': 'paid', 'price': 2500.00},
        {'booking': bookings[2], 'schedule': schedules[1], 'seat_number': 8, 'status': 'booked', 'price': 1800.00},
    ]
    
    tickets = []
    for ticket_data in tickets_data:
        ticket = Ticket.objects.create(**ticket_data)
        tickets.append(ticket)
    
    print(f"Создано {len(tickets)} билетов")
    
    # Создание платежей
    try:
        payment1 = Payment.objects.create(
            booking=bookings[1],
            amount=2500.00,
            payment_method='paypal',
            status='completed',
            transaction_id='PAYPAL_123456'
        )
        
        payment2 = Payment.objects.create(
            booking=bookings[0],
            amount=1800.00,
            payment_method='lipay',
            status='pending',
            transaction_id='LIPAY_789012'
        )
        
        print(f"Создано 2 платежа")
    except Exception as e:
        print(f"Ошибка при создании платежей: {e}")
        print("Пропускаем создание платежей")
    
    print("База данных успешно очищена и заполнена правильными данными!")

if __name__ == "__main__":
    clean_and_fill_database()
