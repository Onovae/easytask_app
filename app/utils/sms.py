import requests
from app.core.config import get_settings
import random
from twilio.rest import Client
from app.core.config import get_settings

settings = get_settings()

# def send_sms(to_number: str, message: str):
#     url = "https://api.brevo.com/v3/transactionalSMS/sms"
#     headers = {
#         "accept": "application/json",
#         "api-key": settings.app.BREVO_API_KEY,
#         "content-type": "application/json"
#     }
#     payload = {
#         "sender": settings.app.SMS_SENDER,
#         "recipient": to_number,
#         "content": message,
#         "type": "transactional"
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code != 201:
#         raise Exception(f"SMS sending failed: {response.status_code} - {response.text}")


# app/utils/sms.py



def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_sms(phone_number: str, otp: str):
    client = Client(settings.app.TWILIO_ACCOUNT_SID, settings.app.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your EasyTask verification code is: {otp}",
        from_=settings.app.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid
