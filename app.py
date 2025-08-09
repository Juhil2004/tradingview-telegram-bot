from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Use environment variables (safer than hardcoding)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    message = data.get("message", "TradingView Alert Received!")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
