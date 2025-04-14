# features/trading/order_manager.py
import requests
from config import LIVE_TRADING, ACCESS_TOKEN

def place_order(access_token, symbol, trade_type, quantity):
    """
    Place an order. When LIVE_TRADING is False, the order is simulated.
    When LIVE_TRADING is True, a real order is sent via the Fyers API.
    """
    if not LIVE_TRADING:
        simulated_order = {
            "symbol": symbol,
            "side": "buy" if trade_type == "buy" else "sell",
            "qty": quantity,
            "status": "simulated",
            "message": "Order simulated (forward testing mode)."
        }
        print("Simulated order:", simulated_order)
        return simulated_order

    # Live trading: perform a real API call
    endpoint = "https://api.fyers.in/api/v2/order"  # Adjust endpoint based on Fyers docs
    order_payload = {
        "symbol": symbol,
        "qty": quantity,
        "type": "1",  # Market order type; adjust if needed
        "side": "1" if trade_type == "buy" else "2",
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "disclosedQty": 0,
        "validity": "DAY",
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.post(endpoint, json=order_payload, headers=headers)
        response.raise_for_status()
        print("Live order placed. Response:", response.json())
        return response.json()
    except requests.RequestException as e:
        print("Error placing live order:", e)
        return {"error": str(e)}
