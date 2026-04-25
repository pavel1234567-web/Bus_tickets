#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=== Simple Email Test ===")
print(f"Email backend: {settings.EMAIL_BACKEND}")
print(f"Email host: {settings.EMAIL_HOST}")
print(f"Email port: {settings.EMAIL_PORT}")
print(f"Email use SSL: {settings.EMAIL_USE_SSL}")
print(f"Email user: {settings.EMAIL_HOST_USER}")
print(f"Default from email: {settings.DEFAULT_FROM_EMAIL}")

# Test simple email sending
try:
    print("\n--- Testing simple email ---")
    result = send_mail(
        'Test from BusTickets System',
        'This is a simple test email to verify email configuration is working.',
        settings.DEFAULT_FROM_EMAIL,
        ['test@example.com'],  # Test address
        fail_silently=False,
    )
    print(f"Simple email result: {result}")
    print("SUCCESS: Simple email sent successfully!")
    
except Exception as e:
    print(f"ERROR: Simple email failed: {str(e)}")
    import traceback
    print(f"Full traceback: {traceback.format_exc()}")

print("\n=== Test Complete ===")
