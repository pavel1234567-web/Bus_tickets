#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.contrib.auth.models import User

# Update admin123 user data
user = User.objects.get(username='admin123')
user.first_name = 'Admin'
user.last_name = 'User'
user.email = 'admin123@bustickets.com'
user.save()

print(f'Updated user {user.username}:')
print(f'  First Name: "{user.first_name}"')
print(f'  Last Name: "{user.last_name}"')
print(f'  Email: "{user.email}"')
