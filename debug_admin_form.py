#!/usr/bin/env python
"""
Debug admin form for Bus model.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.admin import BusAdmin
from tickets.models import Bus

def debug_admin_form():
    """Debug admin form configuration"""
    print('=== Отладка формы админ-панели автобусов ===')
    print()
    
    # Проверяем конфигурацию админ-панели
    admin = BusAdmin(Bus, None)
    
    print('1. list_display:', admin.list_display)
    print('2. list_filter:', admin.list_filter)
    print('3. readonly_fields:', admin.readonly_fields)
    print('4. list_editable:', admin.list_editable)
    print()
    
    print('5. fieldsets:')
    for i, (fieldset_name, fieldset_config) in enumerate(admin.fieldsets):
        print(f'   {i+1}. {fieldset_name}: {fieldset_config["fields"]}')
    print()
    
    # Проверяем форму
    print('6. Проверка формы:')
    try:
        bus = Bus.objects.first()
        if bus:
            form = admin.get_form(None, obj=bus)
            print('   Форма создана успешно')
            print('   Поля формы:', list(form.base_fields.keys()))
            
            # Проверяем, есть ли поле seat_layout_config
            if 'seat_layout_config' in form.base_fields:
                print('   + Поле seat_layout_config есть в форме')
                field = form.base_fields['seat_layout_config']
                print(f'   - Тип поля: {type(field)}')
                print(f'   - Label: {field.label}')
                print(f'   - Required: {field.required}')
                print(f'   - Queryset: {field.queryset.count() if hasattr(field, "queryset") else "N/A"}')
            else:
                print('   - Поле seat_layout_config НЕ найдено в форме')
                
        else:
            print('   - Нет автобусов для тестирования')
            
    except Exception as e:
        print(f'   - Ошибка при создании формы: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_admin_form()
