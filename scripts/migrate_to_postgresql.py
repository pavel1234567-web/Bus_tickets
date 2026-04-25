#!/usr/bin/env python
"""
Migration script from SQLite to PostgreSQL
This script migrates data from SQLite database to PostgreSQL database
"""

import os
import sys
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.db import connections, transaction
from django.core.management import call_command
from django.apps import apps
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

class SQLiteToPostgreSQLMigrator:
    def __init__(self):
        self.sqlite_conn = connections['sqlite']
        self.pg_conn = connections['default']
        
    def get_all_models(self):
        """Get all Django models"""
        models = []
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                models.append(model)
        return models
    
    def get_table_data(self, model, connection):
        """Get all data from a table"""
        table_name = model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
    
    def clear_postgres_table(self, model):
        """Clear all data from PostgreSQL table"""
        table_name = model._meta.db_table
        with self.pg_conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name}")
            self.pg_conn.commit()
            print(f"Cleared table {table_name}")
    
    def insert_data_to_postgres(self, model, columns, rows):
        """Insert data into PostgreSQL table"""
        table_name = model._meta.db_table
        
        # Reset PostgreSQL sequence
        with self.pg_conn.cursor() as cursor:
            cursor.execute(f"""
                ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;
            """)
            self.pg_conn.commit()
        
        # Insert data
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"""
            INSERT INTO {table_name} ({', '.join(columns)}) 
            VALUES ({placeholders})
        """
        
        with self.pg_conn.cursor() as cursor:
            for row in rows:
                try:
                    cursor.execute(insert_query, row)
                except Exception as e:
                    print(f"Error inserting row into {table_name}: {e}")
                    print(f"Row data: {row}")
                    continue
            self.pg_conn.commit()
            print(f"Inserted {len(rows)} rows into {table_name}")
    
    def migrate_model(self, model):
        """Migrate a single model"""
        print(f"\n=== Migrating {model._meta.label} ===")
        
        try:
            # Get data from SQLite
            columns, rows = self.get_table_data(model, self.sqlite_conn)
            print(f"Found {len(rows)} rows in {model._meta.db_table}")
            
            if not rows:
                print(f"No data to migrate for {model._meta.label}")
                return
            
            # Clear PostgreSQL table
            self.clear_postgres_table(model)
            
            # Insert data into PostgreSQL
            self.insert_data_to_postgres(model, columns, rows)
            
            print(f"Successfully migrated {model._meta.label}")
            
        except Exception as e:
            print(f"Error migrating {model._meta.label}: {e}")
    
    def migrate_all(self):
        """Migrate all models"""
        print("Starting migration from SQLite to PostgreSQL...")
        
        # Get all models in dependency order
        models = self.get_all_models()
        
        # Sort models by foreign key dependencies (simple approach)
        # This is a basic ordering - you may need to adjust for complex relationships
        model_order = [
            'auth.User',
            'tickets.Route',
            'tickets.Bus',
            'tickets.Schedule',
            'tickets.Ticket',
            'tickets.Booking',
            'tickets.Payment',
        ]
        
        # Create ordered model list
        ordered_models = []
        for model_label in model_order:
            try:
                app_label, model_name = model_label.split('.')
                model = apps.get_model(app_label, model_name)
                ordered_models.append(model)
            except LookupError:
                print(f"Model {model_label} not found, skipping...")
                continue
        
        # Add any remaining models
        for model in models:
            if model not in ordered_models:
                ordered_models.append(model)
        
        # Migrate each model
        for model in ordered_models:
            self.migrate_model(model)
        
        print("\n=== Migration completed ===")

def create_postgres_database():
    """Create PostgreSQL database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (default database)
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='your_postgres_password_here',
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE bus_tickets_db")
        print("Created database bus_tickets_db")
        
        conn.close()
        
    except psycopg2.errors.DuplicateDatabase:
        print("Database bus_tickets_db already exists")
    except Exception as e:
        print(f"Error creating database: {e}")

def main():
    """Main migration function"""
    print("SQLite to PostgreSQL Migration Script")
    print("=" * 40)
    
    # Create database if needed
    create_postgres_database()
    
    # Run migrations to create tables
    print("\n=== Running Django migrations ===")
    call_command('migrate')
    
    # Start migration
    migrator = SQLiteToPostgreSQLMigrator()
    migrator.migrate_all()
    
    print("\n=== Migration finished successfully! ===")
    print("You can now switch to PostgreSQL by setting USE_SQLITE=False in .env")

if __name__ == '__main__':
    main()
