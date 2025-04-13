# app/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading
import time

from clients.fyers_client import FyersAPIClient
from strategies.breakout_strategy import BreakoutStrategy
from trading.order_manager import place_order
from streaming.live_data import live_data_stream_simulator, live_candles

app = FastAPI(title="Trade Engine API")

# Global simulation variables
orders = []
performance = {"profit": 0, "loss": 0, "net": 0}
risk_management_threshold = -100  # Example risk limit

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("ui/dashboard.html", "r") as f:
        return f.read()

@app.get("/api/performance")
def get_performance():
    return performance

@app.get("/api/orders")
def get_orders():
    return orders

def live_trading_runner():
    access_token = "<YOUR_ACCESS_TOKEN>"  # Replace with your Fyers API token
    symbol = "NSE:SBIN"
    strategy = BreakoutStrategy(parameters={"dummy": True})
    while True:
        try:
            # Ensure we have at least 15 minutes of data
            if len(live_candles) < 15:
                time.sleep(10)
                continue

            recent_data = live_candles[-15:]
            signals = strategy.generate_signals(recent_data)
            for signal in signals:
                if signal["signal"]:
                    if performance["net"] < risk_management_threshold:
                        print("Risk threshold reached. No trades executed.")
                        continue

                    print(f"Breakout in group {signal['group']} with signal {signal['signal']}")
                    if signal["signal"] == "buy":
                        performance["profit"] += 5  # Simulated profit increment
                    else:
                        performance["loss"] += 5   # Simulated loss increment
                    performance["net"] = performance["profit"] - performance["loss"]

                    order = place_order(access_token, symbol, signal["signal"], 10)
                    orders.append(order)
                    print("Order result:", order)
            time.sleep(60)
        except Exception as e:
            print(f"Error in live trading runner: {e}")
            time.sleep(60)

def start_background_tasks():
    threading.Thread(target=live_data_stream_simulator, daemon=True).start()
    threading.Thread(target=live_trading_runner, daemon=True).start()

if __name__ == "__main__":
    start_background_tasks()
    uvicorn.run(app, host="0.0.0.0", port=8000)
