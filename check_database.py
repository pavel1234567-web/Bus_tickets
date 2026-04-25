#!/usr/bin/env python3
"""
Скрипт для проверки таблиц базы данных на правильное заполнение данными
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

from tickets.models import Route, Bus, Schedule, Booking, Ticket, Payment
from django.utils import timezone

def check_routes():
    """Проверка таблицы Routes"""
    print("=== Проверка Routes ===")
    routes = Route.objects.all()
    print(f"Всего маршрутов: {routes.count()}")
    
    for route in routes[:5]:  # Показываем первые 5
        print(f"  {route.name}: {route.departure_city} -> {route.arrival_city}")
        print(f"    Расстояние: {route.distance} км")
        print(f"    Базовая цена: {route.base_price} руб")
        print(f"    Дата отправления: {route.departure_date}")
        print(f"    Адрес отправления: {route.departure_address}")
        print(f"    Адрес прибытия: {route.arrival_address}")
        print()
    
    # Проверка на будущие даты
    today = timezone.now().date()
    past_routes = routes.filter(departure_date__lt=today)
    if past_routes.exists():
        print(f"ВНИМАНИЕ: Найдено {past_routes.count()} маршрутов с прошедшими датами")
        for route in past_routes:
            print(f"  {route.name}: {route.departure_date}")
    else:
        print("OK: Все маршруты имеют будущие даты")

def check_buses():
    """Проверка таблицы Buses"""
    print("\n=== Проверка Buses ===")
    buses = Bus.objects.all()
    print(f"Всего автобусов: {buses.count()}")
    
    bus_types = {}
    for bus in buses:
        bus_type = bus.bus_type
        if bus_type not in bus_types:
            bus_types[bus_type] = 0
        bus_types[bus_type] += 1
    
    print("Типы автобусов:")
    for bus_type, count in bus_types.items():
        print(f"  {bus_type}: {count} шт")
    
    # Показываем несколько примеров
    print("\nПримеры автобусов:")
    for bus in buses[:3]:
        print(f"  {bus.registration_number} - {bus.bus_type} ({bus.total_seats} мест)")

def check_schedules():
    """Проверка таблицы Schedules"""
    print("\n=== Проверка Schedules ===")
    schedules = Schedule.objects.all()
    print(f"Всего расписаний: {schedules.count()}")
    
    # Проверка на будущие даты
    now = timezone.now()
    past_schedules = schedules.filter(departure_time__lt=now)
    if past_schedules.exists():
        print(f"ВНИМАНИЕ: Найдено {past_schedules.count()} расписаний с прошедшими датами")
    else:
        print("✅ Все расписания имеют будущие даты")
    
    # Группировка по датам
    schedules_by_date = {}
    for schedule in schedules:
        date = schedule.departure_time.date()
        if date not in schedules_by_date:
            schedules_by_date[date] = 0
        schedules_by_date[date] += 1
    
    print("Расписания по датам:")
    for date, count in sorted(schedules_by_date.items()):
        print(f"  {date}: {count} расписаний")

def check_bookings():
    """Проверка таблицы Bookings"""
    print("\n=== Проверка Bookings ===")
    bookings = Booking.objects.all()
    print(f"Всего бронирований: {bookings.count()}")
    
    paid_bookings = bookings.filter(is_paid=True)
    unpaid_bookings = bookings.filter(is_paid=False)
    
    print(f"Оплаченных: {paid_bookings.count()}")
    print(f"Неоплаченных: {unpaid_bookings.count()}")
    
    # Показываем последние бронирования
    print("\nПоследние бронирования:")
    for booking in bookings.order_by('-created_at')[:3]:
        print(f"  {booking.booking_reference}: {booking.first_name} {booking.last_name}")
        print(f"    Email: {booking.email}")
        print(f"    Сумма: {booking.total_price} руб")
        print(f"    Статус: {'Оплачено' if booking.is_paid else 'Не оплачено'}")

def check_tickets():
    """Проверка таблицы Tickets"""
    print("\n=== Проверка Tickets ===")
    tickets = Ticket.objects.all()
    print(f"Всего билетов: {tickets.count()}")
    
    paid_tickets = tickets.filter(status='paid')
    booked_tickets = tickets.filter(status='booked')
    
    print(f"Оплаченных билетов: {paid_tickets.count()}")
    print(f"Забронированных билетов: {booked_tickets.count()}")
    
    # Проверка связи с бронированиями
    tickets_without_booking = tickets.filter(booking__isnull=True)
    if tickets_without_booking.exists():
        print(f"ВНИМАНИЕ: Найдено {tickets_without_booking.count()} билетов без бронирования")
    else:
        print("✅ Все билеты связаны с бронированиями")

def check_payments():
    """Проверка таблицы Payments"""
    print("\n=== Проверка Payments ===")
    payments = Payment.objects.all()
    print(f"Всего платежей: {payments.count()}")
    
    completed_payments = payments.filter(status='completed')
    pending_payments = payments.filter(status='pending')
    failed_payments = payments.filter(status='failed')
    
    print(f"Завершенных: {completed_payments.count()}")
    print(f"В ожидании: {pending_payments.count()}")
    print(f"Неудачных: {failed_payments.count()}")
    
    # Показываем последние платежи
    print("\nПоследние платежи:")
    for payment in payments.order_by('-created_at')[:3]:
        print(f"  {payment.transaction_id}: {payment.amount} руб")
        print(f"    Метод: {payment.payment_method}")
        print(f"    Статус: {payment.status}")

def check_integrity():
    """Проверка целостности данных"""
    print("\n=== Проверка целостности данных ===")
    
    # Проверка внешних ключей
    tickets_without_booking = Ticket.objects.filter(booking__isnull=True).count()
    tickets_without_schedule = Ticket.objects.filter(schedule__isnull=True).count()
    schedules_without_route = Schedule.objects.filter(route__isnull=True).count()
    schedules_without_bus = Schedule.objects.filter(bus__isnull=True).count()
    payments_without_booking = Payment.objects.filter(booking__isnull=True).count()
    
    print("Проверка внешних ключей:")
    print(f"  Билеты без бронирования: {tickets_without_booking}")
    print(f"  Билеты без расписания: {tickets_without_schedule}")
    print(f"  Расписания без маршрута: {schedules_without_route}")
    print(f"  Расписания без автобуса: {schedules_without_bus}")
    print(f"  Платежи без бронирования: {payments_without_booking}")
    
    if all(x == 0 for x in [tickets_without_booking, tickets_without_schedule, schedules_without_route, schedules_without_bus, payments_without_booking]):
        print("✅ Целостность внешних ключей в норме")
    else:
        print("❌ Обнаружены проблемы с целостностью данных")

def main():
    """Главная функция"""
    print("Проверка таблиц базы данных")
    print("=" * 50)
    
    try:
        check_routes()
        check_buses()
        check_schedules()
        check_bookings()
        check_tickets()
        check_payments()
        check_integrity()
        
        print("\n" + "=" * 50)
        print("Проверка завершена")
        
    except Exception as e:
        print(f"ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
