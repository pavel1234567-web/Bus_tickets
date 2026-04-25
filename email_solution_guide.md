# Email Sending Solution Guide

## Current Problem
Email sending fails for anonymous users with message: "Booking confirmed! Email sending failed. Please download your PDF ticket below."

## Quick Solution (Temporary)
Switch to console backend to make system work while email is being configured:

### Step 1: Update settings.py
```python
# Temporarily switch to console backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Keep these settings for when we switch back
EMAIL_HOST = 'smtp.ukr.net'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'mega-sergey845@ukr.net'
EMAIL_HOST_PASSWORD = 'hMwaJPK5fBROGu39'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### Step 2: Test the system
1. Restart Django server
2. Try booking as anonymous user
3. Check console for email content
4. Verify PDF download works

## Permanent Solutions

### Option 1: Fix ukr.net Configuration
Ukr.net often requires:
1. **App-specific password** instead of regular password
2. **Two-factor authentication** enabled
3. **Correct SMTP settings**

#### Generate App Password for ukr.net:
1. Go to ukr.net account settings
2. Enable 2FA if not already enabled
3. Generate app-specific password
4. Use that password in EMAIL_HOST_PASSWORD

#### Test ukr.net settings:
```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.ukr.net'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'mega-sergey845@ukr.net'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### Option 2: Use Gmail SMTP (Recommended)
More reliable and better documented:

#### Setup Gmail:
1. Enable 2FA on Gmail account
2. Generate app-specific password
3. Update settings.py:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-gmail-app-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### Option 3: Use Email Service (Production-ready)
Services like SendGrid, Mailgun, or Amazon SES:

#### SendGrid Example:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
DEFAULT_FROM_EMAIL = 'your-verified-sender@domain.com'
```

## Testing Email Configuration

### Method 1: Use test endpoint
Access: `http://localhost:8000/tickets/test-email/`

### Method 2: Run test scripts
```bash
python test_email_simple.py
python test_alternative_email.py
```

### Method 3: Django shell
```python
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

## Current System Status
✅ Working:
- Booking creation for anonymous users
- PDF generation and download
- Error handling and user messages
- Debug logging

⚠️ Needs attention:
- Email server configuration
- SMTP authentication with ukr.net

## User Experience
Even with email issues, users can:
- ✅ Complete booking process
- ✅ Download PDF tickets immediately
- ✅ Get booking reference number
- ✅ Access booking details

## Next Steps
1. Apply quick fix (console backend) for immediate functionality
2. Configure proper email service (Gmail recommended)
3. Test email sending thoroughly
4. Monitor email delivery success rate

## Console Backend Benefits
- System works immediately
- Email content visible in console for debugging
- No dependency on external email services
- Easy to switch back when email is configured
