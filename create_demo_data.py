#!/usr/bin/env python
"""
Script to create demo data for bus seat layouts
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import BusSeatLayout, BusSeat, Bus

def create_demo_data():
    """Create demo bus seat layouts and seats"""
    
    # Create a standard bus layout
    layout, created = BusSeatLayout.objects.get_or_create(
        name="Стандартный автобус 40 мест",
        defaults={
            'description': 'Стандартная компоновка для городского автобуса',
            'total_rows': 10,
            'seats_per_row_left': 2,
            'seats_per_row_right': 2,
            'has_aisle': True,
            'aisle_width': 1,
            'is_active': True
        }
    )
    
    if created:
        print(f"Created layout: {layout}")
        
        # Create seats for this layout
        seat_number = 1
        for row in range(1, layout.total_rows + 1):
            # Left side seats (A, B)
            for seat_in_row in range(1, layout.seats_per_row_left + 1):
                BusSeat.objects.create(
                    layout=layout,
                    row_number=row,
                    position_in_row=seat_in_row,
                    seat_number=seat_number,
                    seat_type='regular',
                    is_available=True,
                    price_multiplier=1.0
                )
                seat_number += 1
            
            # Right side seats (C, D)
            right_start = layout.seats_per_row_left + (1 if layout.has_aisle else 0)
            for seat_in_row in range(right_start, right_start + layout.seats_per_row_right):
                BusSeat.objects.create(
                    layout=layout,
                    row_number=row,
                    position_in_row=seat_in_row,
                    seat_number=seat_number,
                    seat_type='regular',
                    is_available=True,
                    price_multiplier=1.0
                )
                seat_number += 1
        
        print(f"Created {layout.total_seats} seats for layout {layout.name}")
    else:
        print(f"Layout {layout.name} already exists")
    
    # Create a premium bus layout
    premium_layout, created = BusSeatLayout.objects.get_or_create(
        name="Премиум автобус 30 мест",
        defaults={
            'description': 'Премиум компоновка с увеличенным пространством',
            'total_rows': 8,
            'seats_per_row_left': 2,
            'seats_per_row_right': 1,
            'has_aisle': True,
            'aisle_width': 2,
            'is_active': True
        }
    )
    
    if created:
        print(f"Created premium layout: {premium_layout}")
        
        # Create seats for premium layout
        seat_number = 1
        for row in range(1, premium_layout.total_rows + 1):
            # Left side seats (A, B) - make some premium
            for seat_in_row in range(1, premium_layout.seats_per_row_left + 1):
                seat_type = 'premium' if row <= 2 else 'regular'  # First 2 rows are premium
                BusSeat.objects.create(
                    layout=premium_layout,
                    row_number=row,
                    position_in_row=seat_in_row,
                    seat_number=seat_number,
                    seat_type=seat_type,
                    is_available=True,
                    price_multiplier=1.5 if seat_type == 'premium' else 1.0
                )
                seat_number += 1
            
            # Right side seat (C)
            right_start = premium_layout.seats_per_row_left + (1 if premium_layout.has_aisle else 0)
            for seat_in_row in range(right_start, right_start + premium_layout.seats_per_row_right):
                seat_type = 'premium' if row <= 2 else 'regular'
                BusSeat.objects.create(
                    layout=premium_layout,
                    row_number=row,
                    position_in_row=seat_in_row,
                    seat_number=seat_number,
                    seat_type=seat_type,
                    is_available=True,
                    price_multiplier=1.5 if seat_type == 'premium' else 1.0
                )
                seat_number += 1
        
        print(f"Created {premium_layout.total_seats} seats for premium layout {premium_layout.name}")
    else:
        print(f"Premium layout {premium_layout.name} already exists")
    
    # Update existing buses to use layouts
    buses = Bus.objects.filter(seat_layout__isnull=True)[:2]  # Update first 2 buses
    
    for i, bus in enumerate(buses):
        if i == 0:
            bus.seat_layout = layout
            bus.total_seats = layout.total_seats
            bus.seats_per_row = layout.seats_per_row
        else:
            bus.seat_layout = premium_layout
            bus.total_seats = premium_layout.total_seats
            bus.seats_per_row = premium_layout.seats_per_row
        
        bus.save()
        print(f"Updated bus {bus.registration_number} with layout {bus.seat_layout.name}")
    
    print("\nDemo data creation completed!")

if __name__ == "__main__":
    create_demo_data()
