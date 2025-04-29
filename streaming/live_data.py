# features/market_data/live_data.py
import asyncio
import json
from features.fyers.fyers_websocket import listen_to_market_data
from config import ACCESS_TOKEN

# Global list to store live candles; these will be used by the forward tester.
live_candles = []

def process_candle_data(message):
    
    # Process incoming WebSocket message containing candle data.
    # Expected message format (JSON): 
    #     {"time": "YYYY-MM-DD HH:MM:SS", "open": ..., "high": ..., "low": ..., "close": ...}
    
    try:
        # If message is string, parse it as JSON
        data = message if isinstance(message, dict) else json.loads(message)
        candle = {
            "time": data.get("time"),
            "open": float(data.get("open")),
            "high": float(data.get("high")),
            "low": float(data.get("low")),
            "close": float(data.get("close"))
        }
        live_candles.append(candle)
        if len(live_candles) > 100:
            live_candles.pop(0)
        print("Received candle via WebSocket:", candle)
    except Exception as e:
        print("Error processing candle data:", e)

async def listen_live_data_ws(access_token, subscribe_data):
    
    # Async function that connects to the Fyers WebSocket,
    # subscribes to live data, and processes incoming messages.
    
    import websockets
    websocket_url = "wss://api.fyers.in/socket/v2/data"  # Adjust per Fyers documentation
    async with websockets.connect(
            websocket_url,
            extra_headers={"Authorization": f"Bearer {access_token}"}
        ) as websocket:
        await websocket.send(json.dumps(subscribe_data))
        print("Subscribed to live data via WebSocket")
        while True:
            try:
                message = await websocket.recv()
                process_candle_data(message)
            except Exception as e:
                print("WebSocket error in live data:", e)
                break

def live_data_stream_ws():
    
    # Starts the live data stream via WebSocket. This function runs an asyncio loop
    # to listen for incoming candle data from the Fyers WebSocket endpoint.
    
    subscribe_message = {
        "symbols": ["NSE:SBIN"],  # Example symbol; adjust as needed
        "dataType": "candles",    # Specify the type of data you expect
        "resolution": "1"         # 1-minute candles
    }
    asyncio.run(listen_live_data_ws(ACCESS_TOKEN, subscribe_message))
