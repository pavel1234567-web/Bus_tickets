#!/usr/bin/env python
"""
Script to add seat_layout field to Bus table manually
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.db import connection

def add_seat_layout_field():
    """Add seat_layout field to tickets_bus table"""
    
    with connection.cursor() as cursor:
        # Check if field already exists
        cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'tickets_bus' AND column_name = 'seat_layout_id'
        """)
        if cursor.fetchone():
            print("seat_layout_id field already exists!")
            return
        
        # Add the field
        cursor.execute("""
        ALTER TABLE tickets_bus 
        ADD COLUMN seat_layout_id INTEGER 
        REFERENCES tickets_busseatlayout(id) ON DELETE SET NULL
        """)
        
        print("seat_layout_id field added successfully!")

if __name__ == "__main__":
    add_seat_layout_field()
