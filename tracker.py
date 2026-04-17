from flask import Flask, request, redirect, jsonify
import requests as req
import os

app = Flask(__name__)

# This is the "Heartbeat" to tell Railway the app is alive
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/track")
def track():
    brand        = request.args.get("brand", "unknown")
    email_addr   = request.args.get("email", "unknown")
    link_type    = request.args.get("type", "link")
    redirect_url = request.args.get("redirect", "https://zodiac.nitrocommerce.ai/")

    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_KEY", "")

    if url and key:
        try:
            # We use a f-string to ensure the URL is built correctly
            req.post(
                f"{url.rstrip('/')}/rest/v1/email_clicks",
                headers={
                    "apikey": key,
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "brand": brand,
                    "email_addr": email_addr,
                    "link_type": link_type,
                    "clicked": 1
                },
                timeout=5
            )
        except Exception as e:
            print(f"Database Save Error: {e}")

    return redirect(redirect_url)

if __name__ == "__main__":
    # Railway tells the app which port to use via the PORT variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
