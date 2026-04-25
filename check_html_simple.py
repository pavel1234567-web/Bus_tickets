#!/usr/bin/env python
"""
Simple HTML check for seat layout field.
"""

import os

def check_html():
    """Check if admin debug page exists and contains seat layout field"""
    print('=== Проверка HTML файла ===')
    print()
    
    if os.path.exists('admin_debug_page.html'):
        with open('admin_debug_page.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'seat_layout_config' in content:
            print('+ Поле seat_layout_config найдено в HTML')
        else:
            print('- Поле seat_layout_config НЕ найдено в HTML')
            
        if '<select' in content:
            print('+ Select элементы найдены в HTML')
        else:
            print('- Select элементы НЕ найдены в HTML')
            
        # Ищем form элементы
        if '<form' in content:
            print('+ Form элементы найдены в HTML')
        else:
            print('- Form элементы НЕ найдены в HTML')
    else:
        print('Файл admin_debug_page.html не найден')

if __name__ == '__main__':
    check_html()
