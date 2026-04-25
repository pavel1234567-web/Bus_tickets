#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

print("=== Email Configuration Check ===")
print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not configured')}")
print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not configured')}")
print(f"EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', 'Not configured')}")
print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not configured')}")
print(f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'Not configured')}")
print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not configured')}")

print("\n=== Testing Email Sending ===")
try:
    result = send_mail(
        'Test Email from BusTickets',
        'This is a test email to verify email configuration.',
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'test@example.com'),
        ['test@example.com'],
        fail_silently=False,
    )
    print(f"Email sent successfully. Result: {result}")
except Exception as e:
    print(f"Email sending failed: {str(e)}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")

print("\n=== Check Complete ===")
