from flask import Flask, request, redirect, jsonify
import requests as req
import os

app = Flask(__name__)

@app.route("/track")
def track():
    brand        = request.args.get("brand", "unknown")
    email_addr   = request.args.get("email", "unknown")
    link_type    = request.args.get("type", "link")
    redirect_url = request.args.get("redirect", "https://zodiac.nitrocommerce.ai/")

    sb_url = os.environ.get("SUPABASE_URL", "")
    sb_key = os.environ.get("SUPABASE_KEY", "")

    if sb_url and sb_key:
        try:
            req.post(
                sb_url + "/rest/v1/email_clicks",
                headers={
                    "apikey": sb_key,
                    "Authorization": "Bearer " + sb_key,
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
            print("Click save error:", e)

    return redirect(redirect_url)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
