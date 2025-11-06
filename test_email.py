import resend
from app.core.config import get_settings

settings = get_settings()

print(f"RESEND_API_KEY: {settings.email.RESEND_API_KEY[:15]}..." if settings.email.RESEND_API_KEY else "NOT SET")
print(f"EMAIL_FROM: {settings.email.EMAIL_FROM}")

resend.api_key = settings.email.RESEND_API_KEY

try:
    # Test with a different email to verify domain allows any recipient
    test_email = "test@example.com"  # Change this to the email you want to test
    
    params = {
        "from": settings.email.EMAIL_FROM,
        "to": [test_email],
        "subject": "EasyTask Test Email",
        "html": "<h1>Test Email</h1><p>If you receive this, email is working!</p>"
    }
    
    print(f"Sending to: {test_email}")
    
    print("\nSending test email...")
    response = resend.Emails.send(params)
    print(f"✅ SUCCESS! Email sent: {response}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print(f"Error type: {type(e)}")
