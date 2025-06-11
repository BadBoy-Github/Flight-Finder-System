
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

dm = DataManager()
fs = FlightSearch()
nm = NotificationManager()

sheet_data = dm.get_data()

deal_dict = {}
today = datetime.now().strftime("%Y-%m-%d")
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

print(f"{'City':<15}{'Original':<12}{'Current':<12}{'Status'}")

for row in sheet_data:
    city_name = row["city"]
    iata_code = row["iataCode"]
    original_price = int(row["lowestPrice"])

    try:
        website_price = fs.get_flight_price("MAA", iata_code, date_from=today, date_to=tomorrow)
    except Exception as e:
        print(f"{city_name}\tERROR\tERROR\tError fetching price: {e}")
        continue

    price_diff = website_price - original_price

    # Determine deal status
    if website_price < original_price:
        status = "GOOD DEAL"
        deal_dict[city_name] = {
            "iataCode": iata_code,
            "original": original_price,
            "website": website_price,
            "diff": abs(price_diff)
        }
    else:
        status = "NO DEAL"

    print(f"{city_name:<15}₹{original_price:<11}₹{website_price:<11}{status}")

# Send the best deal only
if deal_dict:
    # Get city with maximum savings
    print("\nDeal Dictionary:\n", deal_dict)
    best_deal_city = max(deal_dict, key=lambda city: deal_dict[city]["diff"])
    deal = deal_dict[best_deal_city]
    message = (
        f"🔥 Aggressive Deal Found!\n"
        f"City: {best_deal_city}\n"
        f"Original Price: ₹{deal['original']}\n"
        f"Current Price: ₹{deal['website']}\n"
        f"You Save: ₹{deal['diff']}\n"
        f"Book now from MAA to {deal['iataCode']}!"
    )
else:
    message = "Sorry, No aggressive deals right now."

customers = dm.get_customer_emails()
print(customers)
emails = [customer["emailId:"] for customer in customers]
print("[INFO] Emails fetched:", emails)

nm.send_whatsapp(message)
nm.send_emails(emails, message)
