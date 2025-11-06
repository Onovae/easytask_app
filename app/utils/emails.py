
import smtplib
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer
from app.core.config import get_settings
from email.mime.text import MIMEText
import httpx
import resend


settings = get_settings()
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

# Configure Resend API key
if settings.email.RESEND_API_KEY:
    resend.api_key = settings.email.RESEND_API_KEY

def generate_reset_token(email: str) -> str:
    return serializer.dumps(email, salt="reset-password")

def verify_reset_token(token: str, max_age: int = 3600) -> str:
    return serializer.loads(token, salt="reset-password", max_age=max_age)

def send_reset_email(email: str, token: str):
    reset_link = f"https://yourapp.com/reset-password?token={token}"
    msg = EmailMessage()
    msg["Subject"] = "Reset Your EasyTask Password"
    msg["From"] = settings.email.SMTP_FROM
    msg["To"] = email
    msg.set_content(f"Click to reset your password: {reset_link}")

    with smtplib.SMTP(settings.email.SMTP_HOST, settings.email.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.email.SMTP_USER, settings.email.SMTP_PASSWORD)
        server.send_message(msg)


def send_email(to_email: str, subject: str, body: str):
    """
    Send email using Resend (preferred) or fall back to Brevo
    """
    try:
        # Try Resend first (simpler and more reliable)
        if settings.email.RESEND_API_KEY:
            params = {
                "from": settings.email.EMAIL_FROM,
                "to": [to_email],
                "subject": subject,
                "html": body
            }
            
            response = resend.Emails.send(params)
            print(f"✓ Email sent successfully via Resend: {response}")
            return True
        
        # Fall back to Brevo if Resend is not configured
        elif settings.email.BREVO_API_KEY:
            return send_email_with_brevo(to_email, subject, body)
        
        else:
            print("Warning: No email service configured (RESEND_API_KEY or BREVO_API_KEY)")
            return False
            
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise Exception(f"Email sending failed: {str(e)}")

def send_email_with_brevo(to_email: str, subject: str, body: str):
    headers = {
        "accept": "application/json",
        "api-key": settings.email.BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {"name": "EasyTask", "email": settings.email.SMTP_FROM},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": body
    }

    response = httpx.post("https://api.brevo.com/v3/smtp/email", headers=headers, json=payload)

    if response.status_code >= 400:
        print(f"Email send error: {response.status_code} - {response.text}")
        raise Exception("Email sending failed.")

    return True