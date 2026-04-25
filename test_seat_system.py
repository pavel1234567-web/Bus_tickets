#!/usr/bin/env python
"""
Simple test for seat system functionality
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import BusSeatLayout, BusSeatingScheme, BusSeat, Bus

def test_system():
    """Test the seat system"""
    
    print("=== Testing Bus Seat System ===")
    
    # Test BusSeatLayout
    layouts = BusSeatLayout.objects.all()
    print(f"BusSeatLayout count: {layouts.count()}")
    
    # Test BusSeatingScheme
    schemes = BusSeatingScheme.objects.all()
    print(f"BusSeatingScheme count: {schemes.count()}")
    
    # Test BusSeat
    seats = BusSeat.objects.all()
    print(f"BusSeat count: {seats.count()}")
    
    # Test Bus
    buses = Bus.objects.all()
    print(f"Bus count: {buses.count()}")
    
    # Show details
    print("\n=== Details ===")
    for layout in layouts:
        print(f"Layout: {layout.name} - {layout.total_seats} seats")
    
    for scheme in schemes:
        scheme_seats = BusSeat.objects.filter(scheme=scheme)
        print(f"Scheme: {scheme.name} - {scheme_seats.count()} seats")
    
    for bus in buses[:2]:
        try:
            if hasattr(bus, 'seat_layout') and bus.seat_layout:
                layout_name = bus.seat_layout.name if hasattr(bus.seat_layout, 'name') else "Unknown"
                print(f"Bus: {bus.registration_number} - Layout: {layout_name}")
            else:
                print(f"Bus: {bus.registration_number} - No layout")
        except Exception as e:
            print(f"Bus: {bus.registration_number} - Error: {e}")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_system()
