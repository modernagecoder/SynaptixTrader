# forward_testing/forward_tester.py

import time
from strategies.breakout_strategy import BreakoutStrategy
from trading.order_manager import place_order
from streaming.live_data import live_candles
from app.config import ACCESS_TOKEN, SYMBOL, RISK_MANAGEMENT_THRESHOLD

class ForwardTester:
    def __init__(self, strategy, update_callback=None):
        
        # :param strategy: An instance of a strategy that has a generate_signals method.
        # :param update_callback: Optional callback to report performance updates.
        
        self.strategy = strategy
        self.update_callback = update_callback
        self.orders = []
        self.performance = {"profit": 0, "loss": 0, "net": 0}

    def run(self):
        
        # Runs the forward testing loop: processes live data, generates signals,
        # applies risk management, and simulates orders.
        
        while True:
            try:
                # Ensure a sufficient batch of live candle data is available (e.g., 15 minutes)
                if len(live_candles) < 15:
                    time.sleep(10)
                    continue

                recent_data = live_candles[-15:]
                signals = self.strategy.generate_signals(recent_data)
                for signal in signals:
                    if signal["signal"]:
                        if self.performance["net"] < RISK_MANAGEMENT_THRESHOLD:
                            print("Risk threshold reached. Forward testing halted temporarily.")
                            continue

                        print(f"Forward Testing Signal: Group {signal['group']}, Signal: {signal['signal']}")
                        # Simulate performance changes
                        if signal["signal"] == "buy":
                            self.performance["profit"] += 5  # Example profit
                        elif signal["signal"] == "sell":
                            self.performance["loss"] += 5   # Example loss
                        self.performance["net"] = self.performance["profit"] - self.performance["loss"]

                        # Simulate placing an order via Fyers API
                        order = place_order(ACCESS_TOKEN, SYMBOL, signal["signal"], 10)
                        self.orders.append(order)
                        print("Simulated order:", order)
                        
                        # Optionally call a callback to update a UI or log the latest metrics.
                        if self.update_callback:
                            self.update_callback(self.performance, self.orders)
                time.sleep(60)  # Wait before processing the next set of data
            except Exception as e:
                print("Error in forward testing:", e)
                time.sleep(60)
