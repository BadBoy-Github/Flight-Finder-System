
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()


class FlightSearch:
    def __init__(self):
        self.api_key = os.getenv("AMADEUS_CLIENT_ID")
        self.api_secret = os.getenv("AMADEUS_CLIENT_SECRET")
        self.access_token = self.get_access_token()
        

    def get_access_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_city_code(self, city_name):
        url = "https://test.api.amadeus.com/v1/reference-data/locations"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "keyword": city_name,
            "subType": "CITY"
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("data", [])

        if not data:
            print(f"[WARN] No IATA code found for city: {city_name}")
            return None

        return data[0]["iataCode"]
    
    def search_flights(self, origin_city_code, destination_city_code):
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        today = datetime.now().date()
        six_months_from_today = today + timedelta(days=180)

        params = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": str(today),
            "returnDate": str(today + timedelta(days=7)),
            "adults": 1,
            "currencyCode": "INR",
            "max": 1
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        try:
            flight = data["data"][0]
            price = flight["price"]["total"]
            departure = flight["itineraries"][0]["segments"][0]["departure"]["at"]
            return {
                "price": price,
                "departure_date": departure,
                "flight_data": flight
            }
        except IndexError:
            print(f"No flights found from {origin_city_code} to {destination_city_code}")
            return None
    
    def get_flight_price(self, origin, destination, date_from, date_to, is_direct=True):
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": date_from,
            "returnDate": (datetime.strptime(date_from, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": "INR",
            "max": 1,
            "nonStop": str(is_direct).lower()
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Safeguard against missing or empty data
        if not data.get("data"):
            if is_direct:
            # Retry with indirect flights
                return self.get_flight_price(origin, destination, date_from, date_to, is_direct=False)
            raise ValueError(f"No flight data found from {origin} to {destination}.")

        try:
            return int(float(data["data"][0]["price"]["total"]))
        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise ValueError(f"Error parsing price for flight from {origin} to {destination}: {e}")
