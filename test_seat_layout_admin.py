#!/usr/bin/env python
"""
Test script to verify seat layout admin functionality.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import SeatLayout, Bus

def test_seat_layout_functionality():
    """Test seat layout functionality"""
    print("Testing seat layout functionality...")
    
    # Test 1: Check if SeatLayout model exists
    try:
        layouts = SeatLayout.objects.all()
        print(f"+ SeatLayout model exists, {layouts.count()} layouts found")
    except Exception as e:
        print(f"- SeatLayout model error: {e}")
        return False
    
    # Test 2: Check if Bus model has seat_layout_config field
    try:
        buses = Bus.objects.all()
        print(f"+ Bus model exists, {buses.count()} buses found")
        
        for bus in buses:
            if hasattr(bus, 'seat_layout_config'):
                layout_name = bus.seat_layout_config.name if bus.seat_layout_config else "Default"
                print(f"  - Bus {bus.registration_number}: {layout_name}")
            else:
                print(f"  - Bus {bus.registration_number}: No seat_layout_config field")
                return False
    except Exception as e:
        print(f"- Bus model error: {e}")
        return False
    
    # Test 3: Test seat layout generation
    try:
        layout = SeatLayout.objects.first()
        if layout:
            layout_data = layout.get_layout_display()
            print(f"+ Layout generation works for '{layout.name}': {len(layout_data)} rows")
        else:
            print("- No layouts found to test generation")
            return False
    except Exception as e:
        print(f"- Layout generation error: {e}")
        return False
    
    # Test 4: Test bus seat layout property
    try:
        bus = Bus.objects.first()
        if bus:
            bus_layout = bus.seat_layout
            print(f"+ Bus seat layout property works: {len(bus_layout)} rows")
        else:
            print("- No buses found to test seat layout property")
            return False
    except Exception as e:
        print(f"- Bus seat layout property error: {e}")
        return False
    
    print("\n+ All tests passed!")
    return True

def show_sample_layouts():
    """Show sample seat layouts"""
    print("\nSample seat layouts:")
    
    layouts = SeatLayout.objects.all()[:2]  # Show first 2 layouts
    for layout in layouts:
        print(f"\n{layout.name} ({layout.total_seats} seats, {layout.seats_per_row} per row):")
        layout_data = layout.get_layout_display()
        
        # Show first 3 rows
        for i, row in enumerate(layout_data[:3]):
            row_str = ""
            for seat in row:
                if seat:
                    row_str += f"{seat:3d}"
                else:
                    row_str += "   "
            print(f"  {row_str}")
        
        if len(layout_data) > 3:
            print(f"  ... (+{len(layout_data)-3} more rows)")

if __name__ == '__main__':
    success = test_seat_layout_functionality()
    if success:
        show_sample_layouts()
    else:
        print("\n- Tests failed!")
