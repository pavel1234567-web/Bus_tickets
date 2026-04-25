#!/usr/bin/env python
"""
Test Bus admin form directly.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.admin.sites import site
from tickets.admin import BusAdmin
from tickets.models import Bus, SeatLayout

def test_bus_admin_form():
    """Test Bus admin form directly"""
    print('=== Тестирование формы Bus admin ===')
    print()
    
    try:
        # Получаем админ класс для Bus
        bus_admin = site._registry.get(Bus)
        print(f'Bus admin класс: {bus_admin}')
        
        # Создаем форму с правильным admin_site
        bus = Bus.objects.first()
        if bus:
            print(f'Тестовый автобус: {bus.registration_number}')
            
            # Создаем форму с admin_site
            form = bus_admin.get_form(request=None, obj=bus)
            print('Форма создана успешно!')
            
            # Проверяем поля формы
            fields = list(form.base_fields.keys())
            print(f'Поля формы: {fields}')
            
            if 'seat_layout_config' in fields:
                print('+ Поле seat_layout_config есть в форме')
                field = form.base_fields['seat_layout_config']
                print(f'  Тип поля: {type(field)}')
                print(f'  Label: {field.label}')
                print(f'  Required: {field.required}')
                
                # Проверяем queryset
                if hasattr(field, 'queryset'):
                    print(f'  Queryset count: {field.queryset.count()}')
                    layouts = field.queryset.all()
                    for layout in layouts[:3]:  # Показываем первые 3
                        print(f'    - {layout.name}')
                else:
                    print('  - Нет queryset')
            else:
                print('- Поле seat_layout_config НЕ найдено в форме')
                print('Доступные поля:', fields)
                
        else:
            print('Нет автобусов для тестирования')
            
    except Exception as e:
        print(f'Ошибка: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_bus_admin_form()
