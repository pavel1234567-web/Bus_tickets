#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.contrib.auth.models import User

# Check user profile data
user = User.objects.order_by('-date_joined').first()
if user:
    print(f'User: {user.username}')
    print(f'  First Name: "{user.first_name}"')
    print(f'  Last Name: "{user.last_name}"')
    print(f'  Email: "{user.email}"')
    print(f'  Is Active: {user.is_active}')
    print(f'  Is Staff: {user.is_staff}')
else:
    print('No users found')

# Check all users
print('\nAll users:')
for u in User.objects.all():
    print(f'  {u.username}: {u.get_full_name() or "No name"} ({u.email or "No email"})')
