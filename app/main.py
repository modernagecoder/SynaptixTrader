# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading

# Import API routes
from routes import router as api_router

# Import background task functions
from streaming.live_data import live_data_stream_simulator
from forward_testing.forward_tester import ForwardTester
from strategies.breakout_strategy import BreakoutStrategy

app = FastAPI(title="Trade Engine API")

# Include our API router
app.include_router(api_router)

# Create a global forward tester instance to be used by API endpoints.
forward_tester_instance = ForwardTester(strategy=BreakoutStrategy(parameters={"dummy": True}))

@app.get("/", response_class=HTMLResponse)
def dashboard():
    # Serve the UI dashboard HTML file.
    with open("features/ui/dashboard.html", "r") as f:
        return f.read()

def start_background_tasks():
    # Start simulating live data
    threading.Thread(target=live_data_stream_simulator, daemon=True).start()
    # Start the forward testing (paper trading) process
    threading.Thread(target=forward_tester_instance.run, daemon=True).start()

if __name__ == "__main__":
    start_background_tasks()
    uvicorn.run(app, host="0.0.0.0", port=8000)
