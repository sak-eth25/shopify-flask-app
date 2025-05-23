from flask import Flask, request, redirect, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 🔧 Replace with your real credentials from Shopify
API_KEY = '337b17bbdb6556bb7ff0cba48519b520'
API_SECRET = '548a75d64405fb927ebe0668891c88be'
SCOPES = 'read_products'

# 🔧 Replace with your Render HTTPS URL
REDIRECT_URI = 'https://shopify-flask-app.onrender.com'

@app.route('/')
def index():
    return 'Hello! To install the app, visit /install?shop=your-store.myshopify.com'

@app.route('/install')
def install():
    shop = request.args.get('shop')
    install_url = (
        f"https://{shop}/admin/oauth/authorize"
        f"?client_id={API_KEY}&scope={SCOPES}&redirect_uri={REDIRECT_URI}"
    )
    return redirect(install_url)

@app.route('/callback')
def callback():
    shop = request.args.get('shop')
    code = request.args.get('code')

    token_url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "code": code
    }

    response = requests.post(token_url, json=payload)
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        session["access_token"] = access_token
        session["shop"] = shop

        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }

        shop_info = requests.get(
            f"https://{shop}/admin/api/2023-10/shop.json", headers=headers
        ).json()

        return f"Hello World! App installed on {shop_info['shop']['name']}"
    else:
        return f"Error: {response.text}", 400

if __name__ == '__main__':
    app.run(debug=True)
