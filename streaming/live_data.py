
import time
import datetime

# Global list to hold live candles
live_candles = []

def live_data_stream_simulator():
    """
    Simulates live 1-minute candle data. 
    For production, replace with actual real-time data (e.g., via WebSockets).
    """
    symbol = "NSE:SBIN"
    while True:
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        simulated_offset = (datetime.datetime.now().second % 5)
        candle = {
            "time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "open": 100 + simulated_offset,
            "high": 101 + simulated_offset,
            "low": 99 + simulated_offset,
            "close": 100 + simulated_offset
        }
        live_candles.append(candle)
        if len(live_candles) > 100:
            live_candles.pop(0)
        print(f"New candle: {candle}")
        time.sleep(60)  # Simulate 1-minute intervals
