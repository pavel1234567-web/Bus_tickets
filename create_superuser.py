#!/usr/bin/env python
"""
Script to create superuser for Bus Tickets System
"""

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    try:
        # Check if admin user already exists
        if User.objects.filter(username='admin').exists():
            print("Admin user already exists")
            return
        
        # Create superuser
        User.objects.create_superuser(
            username='admin',
            email='admin@bustickets.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("Superuser 'admin' created successfully!")
        print("Username: admin")
        print("Password: admin123")
        
        # Create additional test users
        users_data = [
            ('ivan_petrov', 'ivan.petrov@example.com', 'Ivan', 'Petrov'),
            ('maria_ivanova', 'maria.ivanova@example.com', 'Maria', 'Ivanova'),
            ('alexey_sidorov', 'alexey.sidorov@example.com', 'Alexey', 'Sidorov'),
            ('anna_fedorova', 'anna.fedorova@example.com', 'Anna', 'Fedorova'),
        ]
        
        for username, email, first_name, last_name in users_data:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=first_name,
                    last_name=last_name
                )
                print(f"User '{username}' created successfully!")
        
        print("\nAll users created successfully!")
        print("\nLogin credentials:")
        print("Admin: admin / admin123")
        print("Users: ivan_petrov, maria_ivanova, alexey_sidorov, anna_fedorova / password123")
        
    except Exception as e:
        print(f"Error creating users: {e}")

if __name__ == '__main__':
    create_superuser()
