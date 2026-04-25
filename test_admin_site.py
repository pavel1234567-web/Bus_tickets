#!/usr/bin/env python
"""
Test admin site registration.
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
    print('Зарегистрированные модели в admin.site:')
    for model, admin_class in site._registry.items():
        print(f'  - {model.__name__}: {admin_class.__name__}')
    
    print()
    
    # Проверяем конкретные модели
    print('Проверка конкретных моделей:')
    bus_admin = site._registry.get(Bus)
    seat_layout_admin = site._registry.get(SeatLayout)
    
    print(f'  Bus admin: {bus_admin}')
    print(f'  SeatLayout admin: {seat_layout_admin}')
    
    print()
    
    # Проверяем, что admin_site не None
    if bus_admin:
        print(f'  Bus admin.admin_site: {bus_admin.admin_site}')
        print(f'  Bus admin.admin_site == site: {bus_admin.admin_site == site}')
    
    if seat_layout_admin:
        print(f'  SeatLayout admin.admin_site: {seat_layout_admin.admin_site}')
        print(f'  SeatLayout admin.admin_site == site: {seat_layout_admin.admin_site == site}')

if __name__ == '__main__':
    test_admin_site()
