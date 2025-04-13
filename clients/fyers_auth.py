# clients/fyers_auth.py
import webbrowser
import requests

def fyers_login(client_id, redirect_url):
    """
    Opens the Fyers login page in the browser for OAuth login.
    After login, the user should capture the auth code from the redirect URL.
    """
    login_url = (
        f"https://api.fyers.in/api/v2/generate-authcode?"
        f"client_id={client_id}&redirect_uri={redirect_url}&response_type=code&state=sample"
    )
    webbrowser.open(login_url)
    print("Login page opened. After logging in, please copy the auth code from the redirect URL.")

def exchange_auth_code_for_access_token(auth_code, client_id, secret_key, redirect_url):
    """
    Exchanges the auth code for an access token.
    This example reflects a typical OAuth flow; adjust parameters per the Fyers docs.
    """
    token_url = "https://api.fyers.in/api/v2/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": client_id,
        "secret_key": secret_key,
        "redirect_uri": redirect_url
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error exchanging auth code:", response.text)
        return None

# Example usage:
if __name__ == "__main__":
    CLIENT_ID = "YOUR_CLIENT_ID"
    REDIRECT_URL = "http://localhost/callback"  # Must match Fyers app settings
    SECRET_KEY = "YOUR_SECRET_KEY"
    
    fyers_login(CLIENT_ID, REDIRECT_URL)
    # After receiving the auth code via redirect, manually enter it:
    auth_code = input("Enter the auth code from the redirect URL: ")
    access_token = exchange_auth_code_for_access_token(auth_code, CLIENT_ID, SECRET_KEY, REDIRECT_URL)
    print("Access token:", access_token)
