"""
Email Click Tracker Server
Runs on Railway (free). Records every link click, then redirects the user.
"""
from flask import Flask, request, redirect
import requests
import os
from datetime import datetime

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")       # set in Railway
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")       # set in Railway


def save_click(brand, email_addr, link_type):
    """Save a click record to Supabase."""
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/email_clicks",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "brand": brand,
                "email_addr": email_addr,
                "link_type": link_type,
                "clicked": 1,
            },
            timeout=5
        )
        return response.status_code == 201
    except Exception as e:
        print(f"Error saving click: {e}")
        return False


@app.route("/track")
def track():
    """
    URL format:
    https://your-railway-app.up.railway.app/track?brand=Zavya&email=someone@example.com&type=dashboard&redirect=https://z.nitrocommerce.ai/login
    """
    brand = request.args.get("brand", "unknown")
    email_addr = request.args.get("email", "unknown")
    link_type = request.args.get("type", "link")
    redirect_url = request.args.get("redirect", "https://zodiac.nitrocommerce.ai/")

    save_click(brand, email_addr, link_type)

    return redirect(redirect_url)


@app.route("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)