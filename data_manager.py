
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT")

class DataManager:
    def __init__(self):
        self.sheet_data = []

    def get_data(self):
        response = requests.get(SHEETY_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data

    def update_iata_code(self, row_id, iata_code):
        body = {
            "price": {
                "iataCode": iata_code
            }
        }
        response = requests.put(f"{SHEETY_ENDPOINT}/{row_id}", json=body)
        response.raise_for_status()
    
    def get_customer_emails(self):
        response = requests.get(SHEETY_USERS_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        return data["users"]
