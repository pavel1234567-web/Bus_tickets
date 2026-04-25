#!/usr/bin/env python
"""
Script to create demo seat layouts for the bus ticketing system.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tickets.models import SeatLayout, Bus

def create_demo_seat_layouts():
    """Create demo seat layouts"""
    
    layouts = [
        {
            'name': 'Standard 2+2',
            'description': 'Стандартная схема 2+2 для обычных автобусов',
            'total_seats': 40,
            'seats_per_row': 4,
            'layout_data': None  # Will be auto-generated
        },
        {
            'name': 'Minibus 2+3',
            'description': 'Схема для микроавтобусов с расположением 2+3',
            'total_seats': 18,
            'seats_per_row': 5,
            'layout_data': None
        },
        {
            'name': 'Luxury 2+1',
            'description': 'Люкс схема с расположением 2+1 для комфортных поездок',
            'total_seats': 24,
            'seats_per_row': 3,
            'layout_data': None
        },
        {
            'name': 'Double Decker 4+4',
            'description': 'Двухэтажный автобус с широкой схемой 4+4',
            'total_seats': 72,
            'seats_per_row': 8,
            'layout_data': None
        }
    ]
    
    created_layouts = []
    for layout_data in layouts:
        layout, created = SeatLayout.objects.get_or_create(
            name=layout_data['name'],
            defaults=layout_data
        )
        
        if created:
            # Auto-generate layout data
            layout.layout_data = layout.generate_default_layout()
            layout.save()
            created_layouts.append(layout)
            print(f"Created seat layout: {layout.name} ({layout.total_seats} seats)")
        else:
            print(f"Seat layout already exists: {layout.name}")
    
    return created_layouts

def assign_layouts_to_buses():
    """Assign seat layouts to existing buses"""
    layouts = SeatLayout.objects.all()
    buses = Bus.objects.filter(seat_layout_config__isnull=True)
    
    if not layouts.exists():
        print("No seat layouts found. Please create layouts first.")
        return
    
    if not buses.exists():
        print("All buses already have seat layouts assigned.")
        return
    
    for bus in buses:
        # Find suitable layout based on bus capacity
        suitable_layout = None
        for layout in layouts:
            if layout.total_seats == bus.total_seats:
                suitable_layout = layout
                break
        
        if not suitable_layout:
            # Find closest layout
            suitable_layout = min(layouts, key=lambda x: abs(x.total_seats - bus.total_seats))
        
        bus.seat_layout_config = suitable_layout
        bus.save()
        print(f"Assigned layout '{suitable_layout.name}' to bus {bus.registration_number}")

def main():
    """Main function"""
    print("Creating demo seat layouts...")
    
    # Create demo layouts
    create_demo_seat_layouts()
    
    # Assign layouts to buses
    assign_layouts_to_buses()
    
    print("\nSummary:")
    print(f"Total seat layouts: {SeatLayout.objects.count()}")
    print(f"Buses with layouts: {Bus.objects.filter(seat_layout_config__isnull=False).count()}")
    print(f"Buses without layouts: {Bus.objects.filter(seat_layout_config__isnull=True).count()}")
    
    print("\nDemo seat layouts setup complete!")

if __name__ == '__main__':
    main()
