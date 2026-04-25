#!/usr/bin/env python
"""
Script to check existing data
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import BusSeatLayout, BusSeat, Bus

def check_existing_data():
    """Check what data already exists"""
    
    print("=== Bus Seat Layouts ===")
    layouts = BusSeatLayout.objects.all()
    for layout in layouts:
        print(f"  {layout.id}: {layout.name} - {layout.total_rows} rows, {layout.total_seats} seats")
        seats = BusSeat.objects.filter(layout=layout)
        print(f"    Seats in database: {seats.count()}")
        if seats.exists():
            print(f"    Seat numbers: {[s.seat_number for s in seats.order_by('seat_number')[:10]]}...")
    
    print("\n=== Buses ===")
    buses = Bus.objects.all()
    for bus in buses:
        layout_name = bus.seat_layout.name if bus.seat_layout and hasattr(bus.seat_layout, 'name') else "No layout"
        print(f"  {bus.registration_number}: {layout_name} - {bus.total_seats} seats")

if __name__ == "__main__":
    check_existing_data()
