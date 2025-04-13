# clients/fyers_websocket.py
import asyncio
import json
import websockets

async def listen_to_market_data(access_token, subscribe_data):
    """
    Connects to the Fyers WebSocket endpoint, subscribes to market data,
    and continuously prints received data.
    """
    websocket_url = "wss://api.fyers.in/socket/v2/data"  # Adjust according to Fyers documentation
    async with websockets.connect(
        websocket_url,
        extra_headers={"Authorization": f"Bearer {access_token}"}
    ) as websocket:
        # Send a subscription message using the provided subscribe_data
        await websocket.send(json.dumps(subscribe_data))
        print("Subscribed to market data. Waiting for messages...")
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                print("Received market data:", data)
            except Exception as e:
                print("WebSocket error:", e)
                break

def start_websocket(access_token, subscribe_data):
    asyncio.get_event_loop().run_until_complete(
        listen_to_market_data(access_token, subscribe_data)
    )

# Example usage:
if __name__ == "__main__":
    # Replace with your actual access token and subscription details.
    ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
    subscribe_message = {
        "symbols": ["NSE:SBIN"],   # Example: list of symbols to subscribe to
        "dataType": "candles",     # Adjust based on the API's supported types
        "resolution": "1"          # 1-minute candles
    }
    start_websocket(ACCESS_TOKEN, subscribe_message)
