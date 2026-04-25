#!/usr/bin/env python
"""
Test admin with proper request object.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.test import RequestFactory
from tickets.admin import BusAdmin
from tickets.models import Bus, SeatLayout

def test_admin_with_request():
    """Test admin with proper request"""
    print('=== Тестирование админ с правильным request ===')
    print()
    
    try:
        # Создаем fake request с пользователем
        factory = RequestFactory()
        
        # Получаем или создаем суперпользователя
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_superuser': True,
                'is_staff': True
            }
        )
        
        if created:
            user.set_password('admin123')
            user.save()
            print('Создан суперпользователь admin')
        
        # Создаем request
        request = factory.get('/admin/tickets/bus/1/change/')
        request.user = user
        
        # Получаем админ класс
        bus_admin = site._registry.get(Bus)
        print(f'Bus admin: {bus_admin}')
        
        # Создаем форму с правильным request
        bus = Bus.objects.first()
        if bus:
            print(f'Тестовый автобус: {bus.registration_number}')
            
            form = bus_admin.get_form(request=request, obj=bus)
            print('Форма создана успешно!')
            
            # Проверяем поля
            fields = list(form.base_fields.keys())
            print(f'Поля формы: {fields}')
            
            if 'seat_layout_config' in fields:
                print('+ Поле seat_layout_config есть в форме')
                field = form.base_fields['seat_layout_config']
                print(f'  Тип: {type(field)}')
                print(f'  Label: {field.label}')
                print(f'  Required: {field.required}')
                
                if hasattr(field, 'queryset'):
                    print(f'  Queryset count: {field.queryset.count()}')
                    layouts = field.queryset.all()
                    for layout in layouts[:3]:
                        print(f'    - {layout.name}')
                        
                # Проверяем HTML представление поля
                print('  HTML представление поля:')
                print(str(field))
                
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
    test_admin_with_request()
