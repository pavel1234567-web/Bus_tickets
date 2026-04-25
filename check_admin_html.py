#!/usr/bin/env python
"""
Check admin HTML for seat layout field.
"""

import os
import sys
import django
import requests
import re

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import Bus

def check_admin_html():
    """Check admin HTML for seat layout field"""
    print('=== Проверка HTML админ-панели ===')
    print()
    
    # Получаем страницу редактирования автобуса
    try:
        bus = Bus.objects.first()
        if bus:
            url = f'http://127.0.0.1:8000/admin/tickets/bus/{bus.id}/change/'
            print(f'Проверяем URL: {url}')
            
            response = requests.get(url)
            print(f'Статус ответа: {response.status_code}')
            
            if response.status_code == 200:
                html = response.text
                
                # Ищем поле seat_layout_config
                if 'seat_layout_config' in html:
                    print('+ Поле seat_layout_config найдено в HTML')
                    
                    # Ищем select элемент
                    if '<select name="seat_layout_config"' in html:
                        print('+ Select элемент для seat_layout_config найден')
                        
                        # Извлекаем опции
                        import re
                        pattern = r'<select[^>]*name="seat_layout_config"[^>]*>(.*?)</select>'
                        match = re.search(pattern, html, re.DOTALL)
                        if match:
                            select_content = match.group(1)
                            
                            # Ищем option элементы
                            option_pattern = r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)</option>'
                            options = re.findall(option_pattern, select_content)
                            
                            print(f'Найдено опций: {len(options)}')
                            for value, text in options[:5]:  # Показываем первые 5
                                print(f'  - {text.strip()} (value: {value})')
                        else:
                            print('- Не удалось извлечь опции из select')
                    else:
                        print('- Select элемент для seat_layout_config НЕ найден')
                else:
                    print('- Поле seat_layout_config НЕ найдено в HTML')
                    
                # Дополнительная проверка - ищем все select поля
                select_pattern = r'<select[^>]*name="([^"]*)"[^>]*>'
                selects = re.findall(select_pattern, html)
                print(f'Все select поля: {selects}')
                
            else:
                print(f'Ошибка загрузки страницы: {response.status_code}')
        else:
            print('Нет автобусов для проверки')
            
    except Exception as e:
        print(f'Ошибка: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_admin_html()
