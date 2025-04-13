# clients/fyers_client.py
import requests
from utils.logger import log_error

class FyersAPIClient:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.fyers.in/api/v2"

    def get_candles(self, symbol, resolution, range_from, range_to):
        endpoint = f"{self.base_url}/data-candles"
        params = {
            "symbol": symbol,
            "resolution": resolution,
            "date_format": "1",
            "range_from": range_from,
            "range_to": range_to,
            "cont_flag": "1"
        }
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log_error(f"Error fetching candles: {e}")
            return None
