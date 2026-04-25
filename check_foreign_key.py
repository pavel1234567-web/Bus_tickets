#!/usr/bin/env python
"""
Script to check foreign key constraints
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.db import connection

def check_foreign_key():
    """Check foreign key constraints"""
    
    with connection.cursor() as cursor:
        # Check foreign key constraint on tickets_busseat
        cursor.execute("""
        SELECT
            tc.constraint_name,
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name = 'tickets_busseat'
        """)
        
        constraints = cursor.fetchall()
        print("Foreign key constraints for tickets_busseat:")
        for constraint in constraints:
            print(f"  {constraint[0]}: {constraint[1]}.{constraint[2]} -> {constraint[3]}.{constraint[4]}")
        
        # Check data in both tables
        cursor.execute("SELECT COUNT(*) FROM tickets_busseatlayout")
        layout_count = cursor.fetchone()[0]
        print(f"\nBusSeatLayout records: {layout_count}")
        
        cursor.execute("SELECT COUNT(*) FROM tickets_busseatingscheme")
        scheme_count = cursor.fetchone()[0]
        print(f"BusSeatingscheme records: {scheme_count}")
        
        cursor.execute("SELECT DISTINCT scheme_id FROM tickets_busseat")
        scheme_ids = [row[0] for row in cursor.fetchall()]
        print(f"Scheme IDs used in tickets_busseat: {scheme_ids}")

if __name__ == "__main__":
    check_foreign_key()
