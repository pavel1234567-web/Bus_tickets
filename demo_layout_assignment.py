#!/usr/bin/env python
"""
Demo script to show how seat layouts are assigned to buses.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import SeatLayout, Bus

def demo_layout_assignment():
    """Demonstrate seat layout assignment process"""
    print("=== ДЕМОНСТРАЦИЯ: Привязка схемы посадочных мест к автобусу ===")
    print()
    
    # Шаг 1: Показываем доступные схемы
    print("ШАГ 1: Доступные схемы посадочных мест")
    print("=" * 50)
    layouts = SeatLayout.objects.all()
    for i, layout in enumerate(layouts, 1):
        print(f"{i}. {layout.name}")
        print(f"   - Мест: {layout.total_seats}")
        print(f"   - Мест в ряду: {layout.seats_per_row}")
        print(f"   - Описание: {layout.description or 'Нет описания'}")
        print()
    
    # Шаг 2: Показываем автобусы
    print("ШАГ 2: Текущие автобусы")
    print("=" * 50)
    buses = Bus.objects.all()
    for i, bus in enumerate(buses, 1):
        current_layout = bus.seat_layout_config.name if bus.seat_layout_config else "Не назначена"
        print(f"{i}. Автобус {bus.registration_number}")
        print(f"   - Тип: {bus.get_bus_type_display()}")
        print(f"   - Текущая схема: {current_layout}")
        print()
    
    # Шаг 3: Демонстрация изменения схемы
    print("ШАГ 3: Демонстрация изменения схемы")
    print("=" * 50)
    
    # Выбираем первый автобус для демонстрации
    bus = Bus.objects.first()
    if bus:
        print(f"Выбираем автобус: {bus.registration_number}")
        old_layout = bus.seat_layout_config
        old_layout_name = old_layout.name if old_layout else "Не назначена"
        print(f"Текущая схема: {old_layout_name}")
        
        # Находим другую схему для назначения
        new_layout = SeatLayout.objects.exclude(id=old_layout.id if old_layout else None).first()
        if new_layout:
            print(f"Назначаем новую схему: {new_layout.name}")
            
            # Изменяем схему
            bus.seat_layout_config = new_layout
            bus.save()
            
            print(f"+ Схема изменена успешно!")
            print(f"   Новая схема: {new_layout.name}")
            
            # Показываем визуализацию новой схемы
            print("\nВизуализация новой схемы:")
            layout_data = new_layout.get_layout_display()
            for i, row in enumerate(layout_data[:5]):  # Показываем первые 5 рядов
                row_str = ""
                for seat in row:
                    if seat:
                        row_str += f"{seat:3d}"
                    else:
                        row_str += "   "
                print(f"   {row_str}")
            
            if len(layout_data) > 5:
                print(f"   ... (+{len(layout_data)-5} рядов)")
            
            # Возвращаем исходную схему
            print(f"\nВозвращаем исходную схему: {old_layout_name}")
            bus.seat_layout_config = old_layout
            bus.save()
            print("+ Исходная схема восстановлена")
        
    print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")
    print("\nИНСТРУКЦИЯ:")
    print("1. Перейдите в админ-панель: http://127.0.0.1:8000/admin/")
    print("2. Выберите 'Tickets' -> 'Buses'")
    print("3. Нажмите на автобус для редактирования")
    print("4. В поле 'Seat layout' выберите нужную схему")
    print("5. Нажмите 'SAVE'")

if __name__ == '__main__':
    demo_layout_assignment()
