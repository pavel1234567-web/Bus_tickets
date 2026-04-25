#!/usr/bin/env python
"""
Test script to check email sending functionality
"""
import os
import sys
import django

# Add project path
sys.path.append('e:\\Projects\\Bus_tickets')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_tickets.settings')

# Setup Django
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from tickets.models import Booking, User

def test_email_settings():
    """Test email configuration"""
    print("=== Email Configuration ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()

def test_simple_email():
    """Test sending a simple email"""
    print("=== Testing Simple Email ===")
    try:
        result = send_mail(
            'Test Email from Bus Tickets System',
            'This is a test email to verify SMTP configuration is working.',
            settings.DEFAULT_FROM_EMAIL,
            ['mega-sergey845@ukr.net'],  # Send to same address for testing
            fail_silently=False,
        )
        print(f"Simple email sent successfully! Result: {result}")
        return True
    except Exception as e:
        print(f"Simple email failed: {str(e)}")
        return False

def test_booking_email():
    """Test sending booking email"""
    print("=== Testing Booking Email ===")
    
    # Get a test booking
    try:
        booking = Booking.objects.filter(user__isnull=False).first()
        if not booking:
            print("No bookings found for registered users")
            return False
            
        print(f"Testing with booking: {booking.booking_reference}")
        print(f"User email: {booking.user.email}")
        print(f"Booking email: {booking.email}")
        
        # Import the function
        from tickets.views import send_booking_email
        
        # Send booking email
        send_booking_email(booking)
        print("Booking email sent successfully!")
        return True
        
    except Exception as e:
        print(f"Booking email failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_user_emails():
    """Check if users have email addresses"""
    print("=== Checking User Emails ===")
    users = User.objects.filter(is_active=True)[:5]
    
    for user in users:
        print(f"User: {user.username}")
        print(f"  Email: {user.email or 'NO EMAIL'}")
        print(f"  First name: {user.first_name or 'NO FIRST NAME'}")
        print(f"  Last name: {user.last_name or 'NO LAST NAME'}")
        
        # Check bookings
        bookings = Booking.objects.filter(user=user)
        print(f"  Bookings: {bookings.count()}")
        for booking in bookings:
            print(f"    - {booking.booking_reference}: {booking.email or 'NO EMAIL'}")
        print()

if __name__ == '__main__':
    print("Bus Tickets Email Testing Script")
    print("=" * 50)
    
    # Test configuration
    test_email_settings()
    
    # Check user emails
    check_user_emails()
    
    # Test simple email
    simple_success = test_simple_email()
    
    # Test booking email
    booking_success = test_booking_email()
    
    print("\n=== Test Results ===")
    print(f"Simple Email: {'✅ PASSED' if simple_success else '❌ FAILED'}")
    print(f"Booking Email: {'✅ PASSED' if booking_success else '❌ FAILED'}")
    
    if simple_success and booking_success:
        print("\n🎉 All tests passed! Email sending should work.")
    else:
        print("\n⚠️  Some tests failed. Check the configuration.")
