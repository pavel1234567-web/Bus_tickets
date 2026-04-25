#!/usr/bin/env python
"""
Test admin site registration - simple version.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.admin.sites import site
from tickets.models import Bus, SeatLayout

def test_admin_site():
    """Test admin site registration"""
    print('=== Проверка регистрации в админ-сайте ===')
    print()
    
    # Проверяем зарегистрированные модели
    print('Зарегистрированные модели:')
    for model in site._registry.keys():
        print(f'  - {model.__name__}')
    
    print()
    
    # Проверяем конкретные модели
    bus_admin = site._registry.get(Bus)
    seat_layout_admin = site._registry.get(SeatLayout)
    
    print(f'Bus admin найден: {bus_admin is not None}')
    print(f'SeatLayout admin найден: {seat_layout_admin is not None}')
    
    if bus_admin:
        print(f'Bus admin admin_site: {bus_admin.admin_site}')
        print(f'Bus admin admin_site is not None: {bus_admin.admin_site is not None}')

if __name__ == '__main__':
    test_admin_site()
