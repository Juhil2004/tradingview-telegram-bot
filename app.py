import requests
import time
from datetime import datetime
from flask import Flask
from threading import Thread

# ======== KOTAK NEO CONFIG ========
CLIENT_ID = "TfwIXS7YwcTHuD9foRcXUfuPfr0a"  # From DevPortal
CLIENT_SECRET = "wE2UjQdCJaJf2XwCjfuL9dNTN5wa"  # From DevPortal
REFRESH_TOKEN = "60cca199-a9dd-37d4-b584-da44ec779d41"   # From login flow
ACCESS_TOKEN = None  # Will be refreshed automatically

# ======== TELEGRAM CONFIG ========
BOT_TOKEN = "8283571353:AAGYNjlQC_nV0R-BJMiza_KngiYmrpsS9xA"
CHAT_ID = "6573373736"

# ======== SYMBOLS TO WATCH ========
SYMBOLS = ["NSE_EQ|RELIANCE", "NSE_EQ|TCS", "NSE_INDEX|Nifty 50"]

# ======== FLASK APP ========
app = Flask(__name__)
bot_thread = None


# ======== TELEGRAM FUNCTION ========
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print(f"Telegram error: {e}")


# ======== KOTAK API ========
def refresh_access_token():
    global ACCESS_TOKEN
    url = "https://napi.kotaksecurities.com/oauth2/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    }
    try:
        res = requests.post(url, data=payload)
        data = res.json()
        if "access_token" in data:
            ACCESS_TOKEN = data["access_token"]
            print("🔑 Access token refreshed")
        else:
            print("❌ Token refresh error:", data)
    except Exception as e:
        print("Error refreshing token:", e)


def get_ltp(symbol):
    if not ACCESS_TOKEN:
        print("⚠️ No access token yet!")
        return None

    url = f"https://napi.kotaksecurities.com/orders/quote/ltp"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "accept": "application/json"}
    params = {"instrumentCode": symbol}

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        return data.get("data", {}).get("lastPrice")
    except Exception as e:
        print("LTP fetch error:", e)
        return None


# ======== STRATEGY LOOP ========
def trading_loop():
    send_telegram("🚀 Kotak Neo Trading Bot started!")
    refresh_access_token()

    while True:
        for symbol in SYMBOLS:
            price = get_ltp(symbol)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if price:
                msg = f"📊 {symbol}\n💰 LTP: {price}\n🕒 {now}"
                send_telegram(msg)
                print(msg)
        time.sleep(30)  # fetch every 30 sec


# ======== BACKGROUND BOT RUNNER ========
def run_bot():
    trading_loop()


# ======== FLASK ROUTES ========
@app.route('/')
def health():
    return "✅ Kotak Neo Bot Live"


@app.route('/start-bot')
def start_bot():
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = Thread(target=run_bot, daemon=True)
        bot_thread.start()
        return "🚀 Bot started!"
    else:
        return "⚡ Already running"


@app.before_first_request
def auto_start():
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = Thread(target=run_bot, daemon=True)
        bot_thread.start()
        print("🚀 Auto-started bot on Render")
