# Email Sending Troubleshooting Guide

## Problem Description
Anonymous users receive the message: "Booking updated, but email failed to send. You can download PDF instead."

## Common Causes and Solutions

### 1. Email Server Configuration Issues
**Symptoms**: Authentication errors, connection timeouts
**Solutions**:
- Check email server credentials in `settings.py`
- Verify SMTP server is accessible
- Try alternative SMTP settings

### 2. Email Provider Restrictions
**Symptoms**: Emails not delivered, sending blocked
**Solutions**:
- ukr.net may require app-specific passwords
- Check if email provider allows SMTP access
- Consider switching to Gmail SMTP

### 3. Network Issues
**Symptoms**: Connection timeouts, network errors
**Solutions**:
- Check firewall settings
- Verify port 465 is open
- Test with different network

## Testing Email Configuration

### Method 1: Use Test Endpoint
Access: `http://localhost:8000/tickets/test-email/`

This will show:
- Email configuration status
- Test sending results
- Specific error messages

### Method 2: Check Console Logs
When email fails, content is saved to console for manual sending.

## Alternative Solutions

### Option 1: Use Gmail SMTP
Update `settings.py`:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

### Option 2: Use Email Backend for Development
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Option 3: Use Third-party Email Service
Consider services like:
- SendGrid
- Mailgun
- Amazon SES

## Current System Behavior
- ✅ Booking creation works
- ✅ PDF generation works  
- ✅ Email validation works
- ⚠️ Email sending may fail
- ✅ Fallback to PDF download works

## User Experience
Even when email fails, users can:
1. Download PDF tickets immediately
2. Get booking reference number
3. Access booking details page
4. Retry email sending later

## Next Steps
1. Test email configuration using test endpoint
2. Check console logs for detailed error information
3. Consider alternative email providers if needed
4. Monitor email sending success rate
