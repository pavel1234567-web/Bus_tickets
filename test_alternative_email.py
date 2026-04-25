#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')
django.setup()

from django.core.mail import send_mail, get_connection
from django.conf import settings

print("=== Alternative Email Configuration Test ===")

# Test 1: Try with different connection settings
print("\n--- Test 1: Direct connection with custom settings ---")
try:
    connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_ssl=settings.EMAIL_USE_SSL,
        use_tls=False,  # Try without TLS
        timeout=30
    )
    
    result = send_mail(
        'Test with Custom Connection',
        'This is a test with custom SMTP connection settings.',
        settings.DEFAULT_FROM_EMAIL,
        ['test@example.com'],
        connection=connection,
        fail_silently=False,
    )
    print(f"Custom connection result: {result}")
    print("SUCCESS: Custom connection worked!")
    
except Exception as e:
    print(f"ERROR: Custom connection failed: {str(e)}")

# Test 2: Try with TLS instead of SSL
print("\n--- Test 2: Try with TLS instead of SSL ---")
try:
    connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host=settings.EMAIL_HOST,
        port=587,  # Try standard TLS port
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_ssl=False,
        use_tls=True,  # Try TLS
        timeout=30
    )
    
    result = send_mail(
        'Test with TLS',
        'This is a test with TLS instead of SSL.',
        settings.DEFAULT_FROM_EMAIL,
        ['test@example.com'],
        connection=connection,
        fail_silently=False,
    )
    print(f"TLS connection result: {result}")
    print("SUCCESS: TLS connection worked!")
    
except Exception as e:
    print(f"ERROR: TLS connection failed: {str(e)}")

# Test 3: Try Gmail as fallback (if configured)
print("\n--- Test 3: Try Gmail configuration ---")
try:
    # You can modify these settings to test with Gmail
    gmail_connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host='smtp.gmail.com',
        port=587,
        username='your-gmail@gmail.com',  # Replace with actual Gmail
        password='your-app-password',     # Replace with app password
        use_ssl=False,
        use_tls=True,
        timeout=30
    )
    
    result = send_mail(
        'Test with Gmail',
        'This is a test with Gmail SMTP.',
        'your-gmail@gmail.com',
        ['test@example.com'],
        connection=gmail_connection,
        fail_silently=False,
    )
    print(f"Gmail connection result: {result}")
    print("SUCCESS: Gmail connection worked!")
    
except Exception as e:
    print(f"ERROR: Gmail connection failed: {str(e)}")

print("\n=== Alternative Test Complete ===")
