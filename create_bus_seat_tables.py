#!/usr/bin/env python
"""
Script to create BusSeatLayout and BusSeat tables manually
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.db import connection

def create_tables():
    """Create the missing tables manually"""
    
    with connection.cursor() as cursor:
        # Create BusSeatLayout table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets_busseatlayout (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            total_rows INTEGER NOT NULL,
            seats_per_row_left INTEGER DEFAULT 2 NOT NULL,
            seats_per_row_right INTEGER DEFAULT 2 NOT NULL,
            has_aisle BOOLEAN DEFAULT TRUE NOT NULL,
            aisle_width INTEGER DEFAULT 1 NOT NULL,
            is_active BOOLEAN DEFAULT TRUE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
        );
        """)
        
        # Create BusSeat table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets_busseat (
            id SERIAL PRIMARY KEY,
            layout_id INTEGER NOT NULL REFERENCES tickets_busseatlayout(id) ON DELETE CASCADE,
            row_number INTEGER NOT NULL,
            seat_number_in_row INTEGER NOT NULL,
            seat_number INTEGER NOT NULL,
            seat_type VARCHAR(20) DEFAULT 'regular' NOT NULL,
            is_available BOOLEAN DEFAULT TRUE NOT NULL,
            price_multiplier DECIMAL(3,2) DEFAULT 1.0 NOT NULL,
            position_x INTEGER DEFAULT 0 NOT NULL,
            position_y INTEGER DEFAULT 0 NOT NULL,
            UNIQUE(layout_id, seat_number)
        );
        """)
        
        # Create indexes
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS tickets_busseat_layout_id_idx 
        ON tickets_busseat(layout_id);
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS tickets_busseat_row_number_idx 
        ON tickets_busseat(row_number);
        """)
        
        print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
