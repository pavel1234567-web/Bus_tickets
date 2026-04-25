#!/usr/bin/env python
"""
Simple check of admin HTML for seat layout field.
"""

import os
import sys
import django
import requests

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Bus

def check_admin_html_simple():
    """Simple check of admin HTML"""
    print('=== Простая проверка HTML админ-панели ===')
    print()
    
    try:
        bus = Bus.objects.first()
        if bus:
            url = f'http://127.0.0.1:8000/admin/tickets/bus/{bus.id}/change/'
            print(f'Проверяем URL: {url}')
            
            response = requests.get(url)
            print(f'Статус ответа: {response.status_code}')
            
            if response.status_code == 200:
                html = response.text
                
                # Простая проверка наличия поля
                if 'seat_layout_config' in html:
                    print('+ Поле seat_layout_config найдено в HTML')
                else:
                    print('- Поле seat_layout_config НЕ найдено в HTML')
                
                # Проверяем наличие select
                if '<select' in html:
                    print('+ Select элементы найдены в HTML')
                else:
                    print('- Select элементы НЕ найдены в HTML')
                
                # Сохраняем HTML для анализа
                with open('admin_page.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                print('HTML сохранен в файл admin_page.html для анализа')
                
            else:
                print(f'Ошибка загрузки страницы: {response.status_code}')
        else:
            print('Нет автобусов для проверки')
            
    except Exception as e:
        print(f'Ошибка: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_admin_html_simple()
