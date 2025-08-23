from flask import Flask
from threading import Thread
import time
import os
import requests
import json
from datetime import datetime
import random
import math

# ======== TELEGRAM BOT CONFIG ========
BOT_TOKEN = "8283571353:AAGYNjlQC_nV0R-BJMiza_KngiYmrpsS9xA"
CHAT_ID = "6573373736"

# ======== DEMO MODE CONFIG ========
DEMO_MODE = True  # Set to False when you get real API working
DEMO_SYMBOLS = {
    "BANKNIFTY24AUGFUT": {"base_price": 45000, "volatility": 0.02},
    "NIFTY24AUGFUT": {"base_price": 22000, "volatility": 0.015},
    "RELIANCE": {"base_price": 2500, "volatility": 0.01},
    "TCS": {"base_price": 3800, "volatility": 0.008}
}

# ======== SEND MESSAGE TO TELEGRAM ========
def send_telegram_message(message):
    """Send message to Telegram bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"✅ Telegram message sent: {message[:50]}...")
            return True
        else:
            print(f"❌ Failed to send Telegram message: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")
        return False

# ======== GET DEMO MARKET DATA ========
def get_demo_market_data(symbol):
    """Generate realistic demo market data"""
    if symbol not in DEMO_SYMBOLS:
        return None
    
    config = DEMO_SYMBOLS[symbol]
    base_price = config["base_price"]
    volatility = config["volatility"]
    
    # Add some randomness to simulate market movement
    change_percent = random.uniform(-volatility, volatility)
    current_price = base_price * (1 + change_percent)
    
    # Add time-based variation
    time_factor = time.time() % 3600 / 3600  # 0 to 1 over an hour
    current_price += base_price * 0.001 * math.sin(time_factor * 2 * math.pi)
    
    return round(current_price, 2)

# ======== TRADING STRATEGY ========
def check_trading_signals(symbol, ltp):
    """Check if trading signals are triggered"""
    if symbol == "BANKNIFTY24AUGFUT":
        # Bank Nifty strategy
        if ltp > 45000:
            message = f"📈 BUY ALERT! {symbol} is at ₹{ltp:,}\nTarget: ₹{int(ltp * 1.01):,}\nStop Loss: ₹{int(ltp * 0.99):,}"
            send_telegram_message(message)
            return "BUY"
        elif ltp < 44000:
            message = f"📉 SELL ALERT! {symbol} is at ₹{ltp:,}\nTarget: ₹{int(ltp * 0.99):,}\nStop Loss: ₹{int(ltp * 1.01):,}"
            send_telegram_message(message)
            return "SELL"
    
    elif symbol == "NIFTY24AUGFUT":
        # Nifty strategy
        if ltp > 22000:
            message = f"📈 BUY ALERT! {symbol} is at ₹{ltp:,}\nTarget: ₹{int(ltp * 1.01):,}\nStop Loss: ₹{int(ltp * 0.99):,}"
            send_telegram_message(message)
            return "BUY"
        elif ltp < 21800:
            message = f"📉 SELL ALERT! {symbol} is at ₹{ltp:,}\nTarget: ₹{int(ltp * 0.99):,}\nStop Loss: ₹{int(ltp * 1.01):,}"
            send_telegram_message(message)
            return "SELL"
    
    elif symbol in ["RELIANCE", "TCS"]:
        # Stock strategy
        base_price = DEMO_SYMBOLS[symbol]["base_price"]
        if ltp > base_price * 1.02:
            message = f"📈 BUY ALERT! {symbol} is at ₹{ltp:,}\nTarget: ₹{int(ltp * 1.015):,}\nStop Loss: ₹{int(ltp * 0.985):,}"
            send_telegram_message(message)
            return "BUY"
        elif ltp < base_price * 0.98:
            message = f"📉 SELL ALERT! {symbol} is at ₹{ltp:,}\nTarget: ₹{int(ltp * 0.985):,}\nStop Loss: ₹{int(ltp * 1.015):,}"
            send_telegram_message(message)
            return "SELL"
    
    return None

# ======== PORTFOLIO TRACKING ========
class Portfolio:
    def __init__(self):
        self.positions = {}
        self.cash = 100000  # Starting with 1 lakh
        self.trades = []
    
    def add_position(self, symbol, action, quantity, price):
        """Add a trade to portfolio"""
        timestamp = datetime.now()
        trade = {
            "timestamp": timestamp,
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "price": price,
            "value": quantity * price
        }
        
        if action == "BUY":
            if symbol not in self.positions:
                self.positions[symbol] = {"quantity": 0, "avg_price": 0}
            
            current = self.positions[symbol]
            total_quantity = current["quantity"] + quantity
            total_value = (current["quantity"] * current["avg_price"]) + (quantity * price)
            current["avg_price"] = total_value / total_quantity
            current["quantity"] = total_quantity
            
            self.cash -= quantity * price
            
        elif action == "SELL":
            if symbol in self.positions:
                current = self.positions[symbol]
                if current["quantity"] >= quantity:
                    current["quantity"] -= quantity
                    self.cash += quantity * price
                    
                    if current["quantity"] == 0:
                        del self.positions[symbol]
        
        self.trades.append(trade)
        return trade
    
    def get_portfolio_value(self, current_prices):
        """Calculate current portfolio value"""
        total_value = self.cash
        
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                market_value = position["quantity"] * current_prices[symbol]
                total_value += market_value
        
        return total_value
    
    def get_portfolio_summary(self, current_prices):
        """Get portfolio summary for Telegram"""
        total_value = self.get_portfolio_value(current_prices)
        pnl = total_value - 100000  # Starting value
        
        summary = f"💼 PORTFOLIO SUMMARY\n"
        summary += f"Total Value: ₹{total_value:,.2f}\n"
        summary += f"P&L: ₹{pnl:+,.2f} ({pnl/100000*100:+.2f}%)\n"
        summary += f"Cash: ₹{self.cash:,.2f}\n\n"
        
        if self.positions:
            summary += "📊 POSITIONS:\n"
            for symbol, position in self.positions.items():
                if symbol in current_prices:
                    current_price = current_prices[symbol]
                    position_value = position["quantity"] * current_price
                    position_pnl = position_value - (position["quantity"] * position["avg_price"])
                    summary += f"{symbol}: {position['quantity']} @ ₹{current_price:,.2f} (P&L: ₹{position_pnl:+,.2f})\n"
        
        return summary

# ======== MAIN TRADING LOOP ========
def run_demo_trading_bot():
    """Main demo trading bot loop"""
    print("🚀 Starting Kotak Neo Demo Trading Bot...")
    
    # Test Telegram connection
    if not send_telegram_message("🚀 Demo Trading Bot started successfully!"):
        print("❌ Cannot connect to Telegram. Check your bot token and chat ID.")
        return
    
    # Initialize portfolio
    portfolio = Portfolio()
    
    # Trading symbols to monitor
    symbols = list(DEMO_SYMBOLS.keys())
    
    print(f"📊 Monitoring symbols: {', '.join(symbols)}")
    print(f"💰 Starting portfolio value: ₹{portfolio.cash:,.2f}")
    
    # Send initial portfolio status
    current_prices = {symbol: get_demo_market_data(symbol) for symbol in symbols}
    portfolio_summary = portfolio.get_portfolio_summary(current_prices)
    send_telegram_message(portfolio_summary)
    
    while True:
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"\n⏰ {current_time} - Checking market data...")
            
            # Get current prices for all symbols
            current_prices = {}
            signals_triggered = []
            
            for symbol in symbols:
                ltp = get_demo_market_data(symbol)
                if ltp:
                    current_prices[symbol] = ltp
                    print(f"📊 {symbol}: ₹{ltp:,.2f}")
                    
                    # Check for trading signals
                    signal = check_trading_signals(symbol, ltp)
                    if signal:
                        signals_triggered.append((symbol, signal, ltp))
                else:
                    print(f"⚠️ Could not get data for {symbol}")
            
            # Execute trades if signals triggered
            for symbol, action, price in signals_triggered:
                quantity = 1  # Demo: trade 1 lot
                trade = portfolio.add_position(symbol, action, quantity, price)
                
                trade_message = f"🎯 TRADE EXECUTED!\n"
                trade_message += f"Symbol: {symbol}\n"
                trade_message += f"Action: {action}\n"
                trade_message += f"Quantity: {quantity}\n"
                trade_message += f"Price: ₹{price:,.2f}\n"
                trade_message += f"Value: ₹{trade['value']:,.2f}"
                
                send_telegram_message(trade_message)
                print(f"✅ Trade executed: {action} {quantity} {symbol} @ ₹{price:,.2f}")
            
            # Send portfolio update every hour
            if datetime.now().minute == 0:
                portfolio_summary = portfolio.get_portfolio_summary(current_prices)
                send_telegram_message(portfolio_summary)
            
            # Wait before next check
            print("⏳ Waiting 30 seconds before next check...")
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
            send_telegram_message("🛑 Demo trading bot stopped by user")
            
            # Send final portfolio summary
            final_summary = portfolio.get_portfolio_summary(current_prices)
            send_telegram_message(final_summary)
            break
            
        except Exception as e:
            error_msg = f"❌ Error in main loop: {e}"
            print(error_msg)
            send_telegram_message(error_msg)
            time.sleep(60)  # Wait longer on error

# ======== FLASK APP INTEGRATION ========
app = Flask(__name__)
bot_thread = None

# This route will serve as a simple health check.
# Render's system will hit this URL to confirm the service is running.
@app.route('/')
def health_check():
    return 'Bot is running!'

# This function will run your original bot logic in a separate thread.
def run_bot_in_background():
    print("Starting bot in background thread...")
    try:
        # Run your main bot function
        run_demo_trading_bot()
    except Exception as e:
        print(f"❌ Fatal error in background thread: {e}")
        send_telegram_message(f"❌ Fatal error: {e}")

@app.route('/start-bot')
def start_bot():
    global bot_thread
    if bot_thread is None or not bot_thread.is_alive():
        bot_thread = Thread(target=run_bot_in_background, daemon=True)
        bot_thread.start()
        return "🚀 Bot started successfully!"
    else:
        return "⚡ Bot is already running."

# The `if __name__ == "__main__":` block should be at the end.
if __name__ == '__main__':
    # Start your bot logic in a separate thread to keep the main thread free for the Flask app.
    bot_thread = Thread(target=run_bot_in_background)
    bot_thread.start()

    # Get the port from the environment variable provided by Render, defaulting to 10000.
    port = int(os.environ.get('PORT', 10000))
    print(f"Flask app binding to port {port}")
    # Run the Flask app
    app.run(host='0.0.0.0', port=port)