# app/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading

from streaming.live_data import live_data_stream_simulator
from app.config import ACCESS_TOKEN, SYMBOL
from forward_testing.forward_tester import ForwardTester
from strategies.breakout_strategy import BreakoutStrategy

app = FastAPI(title="Trade Engine API")

# Global variables for simulated orders and performance are now inside ForwardTester.
# We still provide endpoints for the UI.

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("ui/dashboard.html", "r") as f:
        return f.read()

@app.get("/api/performance")
def get_performance():
    # For demonstration, we assume forward tester instance exposes its performance.
    return forward_tester_instance.performance

@app.get("/api/orders")
def get_orders():
    return forward_tester_instance.orders

# Create a global instance for demonstration purposes.
forward_tester_instance = ForwardTester(strategy=BreakoutStrategy(parameters={"dummy": True}))

def start_background_tasks():
    # Start the live data simulator.
    threading.Thread(target=live_data_stream_simulator, daemon=True).start()
    # Start the forward testing runner from the dedicated module.
    threading.Thread(target=forward_tester_instance.run, daemon=True).start()

if __name__ == "__main__":
    start_background_tasks()
    uvicorn.run(app, host="0.0.0.0", port=8000)
