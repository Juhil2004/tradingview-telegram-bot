import requests
import time

# === CONFIG ===
ACCESS_TOKEN = "eyJ4NXQiOiJNbUprWWpVMlpETmpNelpqTURBM05UZ3pObUUxTm1NNU1qTXpNR1kyWm1OaFpHUTFNakE1TmciLCJraWQiOiJaalJqTUdRek9URmhPV1EwTm1WallXWTNZemRtWkdOa1pUUmpaVEUxTlRnMFkyWTBZVEUyTlRCaVlURTRNak5tWkRVeE5qZ3pPVGM0TWpGbFkyWXpOUV9SUzI1NiIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJjbGllbnQ3NDk2OSIsImF1dCI6IkFQUExJQ0FUSU9OIiwiYXVkIjoiVGZ3SVhTN1l3Y1RIdUQ5Zm9SY1hVZnVQZnIwYSIsIm5iZiI6MTc1NTE1Nzg4NCwiYXpwIjoiVGZ3SVhTN1l3Y1RIdUQ5Zm9SY1hVZnVQZnIwYSIsInNjb3BlIjoiZGVmYXVsdCIsImlzcyI6Imh0dHBzOlwvXC9uYXBpLmtvdGFrc2VjdXJpdGllcy5jb206NDQzXC9vYXV0aDJcL3Rva2VuIiwiZXhwIjoxNzU1MjQ0Mjg0LCJpYXQiOjE3NTUxNTc4ODQsImp0aSI6ImQwZDM3NTYwLTY4Y2QtNGRlYS04YTA3LTUyM2RiZmYyOTQzZSJ9.amRtRnFTLrhsnZ0T0jeIJrE3kWVsP5H-HMRPkonYtvTRMDvQkhHUsIjGfFFfc73Eatkl5J7w50p8tSXXGbc7gTzsdLAPLDL7hAZiYDuRzoX7E2YTs8PKZK6dE-P2I0DlZGzvlKC4qvsI92SNc-Huz09sTqSJu4nZ3HGwBweqFu8eYEuZ5Vlr-gSZRDr8gwqtun5BLX-hV0vKz5KFx8pajUwBMHrXk_qJ5fqcdD9ymTyQ7bTYzdX4QaUcfiBIKI3LFBEjBnmBA3FjB9YMoGD14PlD6gZUH7zkXnXCeoWBcMAMt0WTndzOiLhP8WlaLjEIwXUIc8NTI5nuRGdH1vUTYA"
TELEGRAM_TOKEN = "8283571353:AAGYNjlQC_nV0R-BJMiza_KngiYmrpsS9xA"
CHAT_ID = "6573373736"
SYMBOL = "BANKNIFTY24AUGFUT"  # Example symbol

# === Function to get LTP from Kotak Neo ===
def get_ltp(symbol):
    url = f"https://apigateway.kotaksecurities.com/market/quote/{symbol}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    r = requests.get(url, headers=headers)
    data = r.json()
    return float(data['data'][0]['last_price'])

# === Function to send Telegram alert ===
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

# === Strategy: Alert if price > 45000 ===
while True:
    try:
        ltp = get_ltp(SYMBOL)
        print(f"LTP: {ltp}")

        if ltp > 45000:
            send_telegram(f"📈 BUY ALERT! {SYMBOL} is at {ltp}")
        elif ltp < 44000:
            send_telegram(f"📉 SELL ALERT! {SYMBOL} is at {ltp}")

        time.sleep(10)  # Fetch every 10 seconds

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
