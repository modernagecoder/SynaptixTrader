# # clients/fyers_client.py
# import requests
# from utils.logger import log_error

# class FyersAPIClient:
#     def __init__(self, access_token):
#         self.access_token = access_token
#         self.base_url = "https://api.fyers.in/api/v2"

#     def get_candles(self, symbol, resolution, range_from, range_to):
#         endpoint = f"{self.base_url}/data-candles"
#         params = {
#             "symbol": symbol,
#             "resolution": resolution,
#             "date_format": "1",
#             "range_from": range_from,
#             "range_to": range_to,
#             "cont_flag": "1"
#         }
#         headers = {"Authorization": f"Bearer {self.access_token}"}
#         try:
#             response = requests.get(endpoint, params=params, headers=headers)
#             response.raise_for_status()
#             return response.json()
#         except requests.RequestException as e:
#             log_error(f"Error fetching candles: {e}")
#             return None

import os
import json
import sys
# Ensure project root is on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fyers_apiv3 import fyersModel

# ─── CONFIG ───────────────────────────────────────────────────────────
CLIENT_ID = "YOUR_CLIENT_ID"  # Same app_id used above
TOKENS_FILE = os.path.join(os.path.dirname(__file__), "tokens.json")
LOG_PATH = os.path.join(os.path.dirname(__file__), "fyers.log")


def load_tokens():
    if not os.path.exists(TOKENS_FILE):
        raise FileNotFoundError(f"Token file not found: {TOKENS_FILE}. Run fyers_auth.py first.")
    with open(TOKENS_FILE) as f:
        return json.load(f)


def main():
    # Load saved tokens
    tokens = load_tokens()
    access_token = tokens.get("access_token")
    if not access_token:
        raise ValueError("No access_token found in tokens.json")

    # Initialize the FYERS client (v3)
    fyers = fyersModel.FyersModel(
        client_id=CLIENT_ID,
        token=access_token,
        is_async=False,
        log_path=LOG_PATH
    )

    # Example calls using v3 endpoints:
    profile = fyers.get_profile()
    print("Profile details:", profile)

    funds = fyers.funds()
    print("Funds details:", funds)

    # Add more calls here (order placement, market data, etc.)


if __name__ == "__main__":
    main()