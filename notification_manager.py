
from twilio.rest import Client
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

CLIENT = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")

class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    
    def send_whatsapp(self, message):
        message = self.client.messages.create(
            from_='whatsapp:' + TWILIO_FROM,
            to='whatsapp:' + TWILIO_TO,
            body=message
        )
        print(f"[WHATSAPP SENT] SID: {message.sid}")
    
    def send_emails(self, emails, message):
        for email in emails:
            with smtplib.SMTP(SMTP_SERVER, 587) as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=EMAIL_PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=email,
                    msg=f"Subject:Flight Deal!\n\n{message}".encode("utf-8")
                )
        print(f"[EMAIL SENT] Sent to {len(emails)} customers.")

                
