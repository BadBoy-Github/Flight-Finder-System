
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

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
