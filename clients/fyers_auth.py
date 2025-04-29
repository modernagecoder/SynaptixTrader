# # clients/fyers_auth.py
# import webbrowser
# import requests
# import app.config as config

# def fyers_login(client_id, redirect_url):
    
#     # Opens the Fyers login page in the browser for OAuth login.
#     # After login, the user should capture the auth code from the redirect URL.
    
#     login_url = (
#         f"https://api.fyers.in/api/v2/generate-authcode?"
#         f"client_id={client_id}&redirect_uri={redirect_url}&response_type=code&state=sample"
#     )
#     webbrowser.open(login_url)
#     print("Login page opened. After logging in, please copy the auth code from the redirect URL.")

# def exchange_auth_code_for_access_token(auth_code, client_id, secret_key, redirect_url):
    
#     # Exchanges the auth code for an access token.
#     # This example reflects a typical OAuth flow; adjust parameters per the Fyers docs.
    
#     token_url = "https://api.fyers.in/api/v2/token"
#     payload = {
#         "grant_type": "authorization_code",
#         "code": auth_code,
#         "client_id": client_id,
#         "secret_key": secret_key,
#         "redirect_uri": redirect_url
#     }
#     response = requests.post(token_url, data=payload)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         print("Error exchanging auth code:", response.text)
#         return None

# # Example usage:
# if __name__ == "__main__":
#     CLIENT_ID = config.CLIENT_ID
#     REDIRECT_URL = config.REDIRECT_URL  # Must match Fyers app settings
#     SECRET_KEY = config.SECRET_KEY
    
#     fyers_login(CLIENT_ID, REDIRECT_URL)
#     # After receiving the auth code via redirect, manually enter it:
#     auth_code = input("Enter the auth code from the redirect URL: ")
#     access_token = exchange_auth_code_for_access_token(auth_code, CLIENT_ID, SECRET_KEY, REDIRECT_URL)
#     print("Access token:", access_token)


import threading
import webbrowser
import time
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from fyers_apiv3 import fyersModel

# ─── CONFIG ───────────────────────────────────────────────────────────
CLIENT_ID    = "YOUR_CLIENT_ID"       # Your FYERS App ID (e.g. XCXXXXXxxM-100)
SECRET_KEY   = "YOUR_SECRET_KEY"      # Your FYERS App Secret
REDIRECT_URI = "http://localhost:8080/callback"
STATE        = "XYZ"                  # Optional state parameter
AUTH_PORT    = 8080

# Initialize a V3 session model
session = fyersModel.SessionModel(
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY,
    redirect_uri=REDIRECT_URI,
    response_type="code",
    state=STATE,
    grant_type="authorization_code"
)

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        # v3 may return 'auth_code' or 'code'
        code = params.get("auth_code", params.get("code", []))
        code = code[0] if code else None
        if code:
            self.server.auth_code = code
            self.send_response(200)
            self.end_headers()
            self.wfile.write("<h1>✅ Authentication successful</h1>\n<p>You can close this window.</p>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("<h1>❌ Auth code missing</h1>")

def get_auth_code_via_http():
    server = HTTPServer(("", AUTH_PORT), AuthHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    auth_url = session.generate_authcode()
    print("Opening browser to:", auth_url)
    webbrowser.open(auth_url, new=1)
    while not hasattr(server, "auth_code"):
        time.sleep(0.5)
    code = server.auth_code
    server.shutdown()
    return code

if __name__ == "__main__":
    # 1) Obtain auth code automatically
    auth_code = get_auth_code_via_http()

    # 2) Exchange for tokens
    session.set_token(auth_code)
    token_response = session.generate_token()

    # 3) Persist tokens
    output = {
        "access_token": token_response.get("access_token"),
        "refresh_token": token_response.get("refresh_token")
    }
    tokens_file = os.path.join(os.path.dirname(__file__), "tokens.json")
    with open(tokens_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Tokens saved to {tokens_file}")