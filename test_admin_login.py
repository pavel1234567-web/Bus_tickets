#!/usr/bin/env python
"""
Test admin login and seat layout field.
"""

import os
import sys
import django
import requests

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import authenticate, login
from django.test import Client
from tickets.models import Bus, SeatLayout

def test_admin_login():
    """Test admin login and seat layout field"""
    print('=== Тестирование входа в админ и поля схем ===')
    print()
    
    # Создаем тестовый клиент
    client = Client()
    
    # Проверяем, есть ли суперпользователь
    from django.contrib.auth.models import User
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
    
    # Выполняем вход
    login_success = client.login(username='admin', password='admin123')
    print(f'Вход в админ: {"успешно" if login_success else "неудачно"}')
    
    if login_success:
        # Проверяем страницу редактирования автобуса
        bus = Bus.objects.first()
        if bus:
            url = f'/admin/tickets/bus/{bus.id}/change/'
            response = client.get(url)
            print(f'Статус страницы редактирования: {response.status_code}')
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                if 'seat_layout_config' in content:
                    print('+ Поле seat_layout_config найдено на странице')
                    
                    # Ищем select элемент
                    if '<select name="seat_layout_config"' in content:
                        print('+ Select элемент для seat_layout_config найден')
                        
                        # Извлекаем опции
                        import re
                        pattern = r'<select[^>]*name="seat_layout_config"[^>]*>(.*?)</select>'
                        match = re.search(pattern, content, re.DOTALL)
                        if match:
                            select_content = match.group(1)
                            
                            # Ищем option элементы
                            option_pattern = r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)</option>'
                            options = re.findall(option_pattern, select_content)
                            
                            print(f'Найдено опций: {len(options)}')
                            for value, text in options[:5]:
                                print(f'  - {text.strip()} (value: {value})')
                        else:
                            print('- Не удалось извлечь опции')
                    else:
                        print('- Select элемент не найден')
                else:
                    print('- Поле seat_layout_config НЕ найдено на странице')
                    
                    # Сохраняем страницу для анализа
                    with open('admin_debug_page.html', 'w', encoding='utf-8') as f:
                        f.write(content)
                    print('Страница сохранена в admin_debug_page.html')
            else:
                print(f'Ошибка загрузки страницы: {response.status_code}')
        else:
            print('Нет автобусов для тестирования')
    else:
        print('Не удалось войти в админ')

if __name__ == '__main__':
    test_admin_login()
