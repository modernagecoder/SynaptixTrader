
import requests
from utils.logger import log_error

def place_order(access_token, symbol, trade_type, quantity):
    """
    Places a simulated order via the Fyers API.
    In production, replace this simulation with real order placement logic.
    """
    endpoint = "https://api.fyers.in/api/v2/order"
    order_payload = {
        "symbol": symbol,
        "qty": quantity,
        "type": "1",  # Market order type; adjust as necessary
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
        return response.json()
    except requests.RequestException as e:
        log_error(f"Error placing order: {e}")
        return {"error": str(e)}
