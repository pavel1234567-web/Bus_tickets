#!/usr/bin/env python
"""
Script to complete demo data for bus seat layouts
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from tickets.models import BusSeatLayout, BusSeat, Bus

def complete_demo_data():
    """Complete demo bus seat layouts and seats"""
    
    # Get the existing layout
    layout = BusSeatLayout.objects.get(id=1)
    print(f"Working with layout: {layout.name}")
    
    # Check existing seats
    existing_seats = BusSeat.objects.filter(layout=layout)
    existing_numbers = set(existing_seats.values_list('seat_number', flat=True))
    print(f"Existing seats: {len(existing_seats)}")
    print(f"Existing seat numbers: {sorted(existing_numbers)}")
    
    # Add missing seats
    total_seats_needed = layout.total_seats
    missing_numbers = set(range(1, total_seats_needed + 1)) - existing_numbers
    print(f"Missing seat numbers: {sorted(missing_numbers)}")
    
    if missing_numbers:
        # Calculate seat positions for missing numbers
        seats_per_row = layout.seats_per_row
        seats_left = layout.seats_per_row_left
        seats_right = layout.seats_per_row_right
        
        for seat_number in sorted(missing_numbers):
            # Calculate row and position
            row = (seat_number - 1) // seats_per_row + 1
            position_in_row = (seat_number - 1) % seats_per_row + 1
            
            # Determine seat type based on position
            seat_type = 'regular'
            if position_in_row <= seats_left:
                # Left side
                pass  # regular
            else:
                # Right side
                pass  # regular
            
            BusSeat.objects.create(
                layout=layout,
                row_number=row,
                position_in_row=position_in_row,
                seat_number=seat_number,
                seat_type=seat_type,
                is_available=True,
                price_multiplier=1.0
            )
            print(f"Created seat {seat_number} at row {row}, position {position_in_row}")
    
    # Update buses to use this layout
    buses = Bus.objects.filter(seat_layout__isnull=True)
    for bus in buses:
        bus.seat_layout = layout
        bus.total_seats = layout.total_seats
        bus.seats_per_row = layout.seats_per_row
        bus.save()
        print(f"Updated bus {bus.registration_number} with layout")
    
    # Create a second layout (premium)
    premium_layout, created = BusSeatLayout.objects.get_or_create(
        name="Премиум автобус 24 места",
        defaults={
            'description': 'Премиум компоновка с увеличенным пространством',
            'total_rows': 6,
            'seats_per_row_left': 2,
            'seats_per_row_right': 2,
            'has_aisle': True,
            'aisle_width': 2,
            'is_active': True
        }
    )
    
    if created:
        print(f"\nCreated premium layout: {premium_layout.name}")
        
        # Create all seats for premium layout
        seat_number = 1
        for row in range(1, premium_layout.total_rows + 1):
            # Left side seats
            for seat_in_row in range(1, premium_layout.seats_per_row_left + 1):
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
            
            # Right side seats
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
        
        print(f"Created {premium_layout.total_seats} seats for premium layout")
        
        # Update one bus to use premium layout
        bus = Bus.objects.first()
        if bus:
            bus.seat_layout = premium_layout
            bus.total_seats = premium_layout.total_seats
            bus.seats_per_row = premium_layout.seats_per_row
            bus.save()
            print(f"Updated bus {bus.registration_number} with premium layout")
    
    print("\nDemo data completion completed!")

if __name__ == "__main__":
    complete_demo_data()
