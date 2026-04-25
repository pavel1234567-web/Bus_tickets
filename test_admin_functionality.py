#!/usr/bin/env python
"""
Script to test admin functionality for bus seat layouts
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import BusSeatLayout, BusSeat, Bus
from tickets.admin import BusSeatLayoutAdmin

def test_admin_functionality():
    """Test admin functionality"""
    
    print("=== Testing Bus Seat Layout Admin ===")
    
    # Test layout creation
    layouts = BusSeatLayout.objects.all()
    print(f"Found {layouts.count()} layouts")
    
    for layout in layouts:
        print(f"\nLayout: {layout.name}")
        print(f"  Total rows: {layout.total_rows}")
        print(f"  Seats per row: {layout.seats_per_row}")
        print(f"  Total seats: {layout.total_seats}")
        
        # Test seats
        seats = BusSeat.objects.filter(layout=layout)
        print(f"  Seats in database: {seats.count()}")
        
        # Test seat layout preview method
        admin_instance = BusSeatLayoutAdmin(BusSeatLayout, None)
        try:
            preview = admin_instance.layout_preview(layout)
            print(f"  Preview generated successfully: {len(preview)} characters")
        except Exception as e:
            print(f"  Preview error: {e}")
    
    print("\n=== Testing Bus Admin ===")
    buses = Bus.objects.all()
    print(f"Found {buses.count()} buses")
    
    for bus in buses[:3]:  # Show first 3 buses
        try:
            layout_info = bus.seat_layout.name if bus.seat_layout and hasattr(bus.seat_layout, 'name') else "No layout"
            print(f"  {bus.registration_number}: {layout_info}")
        except Exception as e:
            print(f"  {bus.registration_number}: Error getting layout - {e}")
    
    print("\n=== Testing Seat Generation ===")
    # Test seat generation for a new layout
    test_layout, created = BusSeatLayout.objects.get_or_create(
        name="Тестовая схема",
        defaults={
            'description': 'Тестовая схема для проверки',
            'total_rows': 3,
            'seats_per_row_left': 1,
            'seats_per_row_right': 1,
            'has_aisle': True,
            'aisle_width': 1,
            'is_active': True
        }
    )
    
    if created:
        print(f"Created test layout: {test_layout.name}")
        
        # Generate seats manually
        seat_number = 1
        for row in range(1, test_layout.total_rows + 1):
            # Left seat
            BusSeat.objects.create(
                layout=test_layout,
                row_number=row,
                position_in_row=1,
                seat_number=seat_number,
                seat_type='regular',
                is_available=True,
                price_multiplier=1.0
            )
            seat_number += 1
            
            # Right seat
            BusSeat.objects.create(
                layout=test_layout,
                row_number=row,
                position_in_row=2,
                seat_number=seat_number,
                seat_type='regular',
                is_available=True,
                price_multiplier=1.0
            )
            seat_number += 1
        
        print(f"Created {test_layout.total_seats} seats for test layout")
        
        # Test seat codes
        seats = BusSeat.objects.filter(layout=test_layout).order_by('seat_number')
        for seat in seats:
            print(f"    Seat {seat.seat_number}: {seat.seat_code} (row {seat.row_number}, type {seat.seat_type})")
    
    print("\n=== Test completed successfully! ===")

if __name__ == "__main__":
    test_admin_functionality()
