#!/usr/bin/env python
"""
Script to check table structures
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.db import connection

def check_structures():
    """Check table structures"""
    
    with connection.cursor() as cursor:
        # Check busseatlayout structure
        print("=== tickets_busseatlayout ===")
        cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'tickets_busseatlayout' 
        ORDER BY ordinal_position
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]} ({row[1]}) nullable={row[2]} default={row[3]}")
        
        # Check busseat structure
        print("\n=== tickets_busseat ===")
        cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'tickets_busseat' 
        ORDER BY ordinal_position
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]} ({row[1]}) nullable={row[2]} default={row[3]}")
        
        # Check busseatingscheme structure (old table)
        print("\n=== tickets_busseatingscheme ===")
        cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'tickets_busseatingscheme' 
        ORDER BY ordinal_position
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]} ({row[1]}) nullable={row[2]} default={row[3]}")

if __name__ == "__main__":
    check_structures()
