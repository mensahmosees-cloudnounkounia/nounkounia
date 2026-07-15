import os
import requests
from flask import Flask, request

app = Flask(__name__)

# === TOKENS - on accepte tout pour éviter le mismatch ===
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "Nounkoun2026").strip()
VERIFY_TOKEN_2 = os.getenv("WHATSAPP_VERIFY_TOKEN", "Nounkoun2026").strip()
# on met les 2 en liste
ALLOWED_TOKENS = [t for t in [VERIFY_TOKEN, VERIFY_TOKEN_2, "Nounkoun2026", "nounkoun2026"] if t]

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "").strip()
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "").strip()

print(f"[BOOT] VERIFY_TOKEN={VERIFY_TOKEN} | VERIFY_TOKEN_2={VERIFY_TOKEN_2}")

@app.route("/", methods=["GET", "HEAD"])
def home():
    return "Nounkounia V8.1 LIVE - META DIRECT OK - Token=Nounkoun2026", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = (request.args.get("hub.verify_token") or "").strip()
    challenge = request.args.get("hub.challenge")

    print(f"[VERIFY] mode={mode} token_recu={token} challenge={challenge} | attendu={ALLOWED_TOKENS}")

    if mode == "subscribe" and token in ALLOWED_TOKENS:
        print("[VERIFY] OK -> renvoi challenge")
        return challenge, 200
    else:
        print("[VERIFY] FAIL -> token mismatch")
        return "token mismatch", 403

@app.route("/webhook", methods=["POST"])
def handle_message():
    data = request.get_json()
    print(f"[WEBHOOK POST] {data}")
    # Logique minimale pour que Meta voit 200 OK
    try:
        if data and data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for msg in messages:
                        from_id = msg.get("from")
                        text = msg.get("text", {}).get("body", "")
                        print(f"Message de {from_id}: {text}")
                        # Ici tu pourras remettre ton bot
    except Exception as e:
        print(f"Erreur handle: {e}")

    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
