#!/usr/bin/env python
"""
Script to check existing tables
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.db import connection

def check_tables():
    """Check what tables exist"""
    
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public' AND tablename LIKE 'tickets_%'
        ORDER BY tablename
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print("Existing tables:")
        for table in tables:
            print(f"  - {table}")
        
        # Check if busseatlayout and busseat tables exist
        if 'tickets_busseatlayout' in tables:
            print("\ntickets_busseatlayout table exists!")
            cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'tickets_busseat' 
            ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print("tickets_busseat columns:")
            for col in columns:
                print(f"  - {col[0]} ({col[1]})")
        else:
            print("\ntickets_busseatlayout table does NOT exist!")

if __name__ == "__main__":
    check_tables()
