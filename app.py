import os
from flask import Flask, request, Response

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "Nounkoun2026").strip()
VERIFY_TOKEN_2 = os.getenv("WHATSAPP_VERIFY_TOKEN", "Nounkoun2026").strip()
ALLOWED_TOKENS = [t for t in [VERIFY_TOKEN, VERIFY_TOKEN_2, "Nounkoun2026", "nounkoun2026"] if t]

print(f"[BOOT] VERIFY_TOKEN={VERIFY_TOKEN}")

@app.route("/", methods=["GET", "HEAD"])
def home():
    return "Nounkounia V8.1 LIVE - META DIRECT OK - Token=Nounkoun2026", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = (request.args.get("hub.verify_token") or "").strip()
        challenge = request.args.get("hub.challenge")
        print(f"[VERIFY] mode={mode} token={token}")
        if mode == "subscribe" and token in ALLOWED_TOKENS:
            return challenge, 200
        return "token mismatch", 403

    try:
        body = (request.values.get("Body","") or request.args.get("Body","") or request.args.get("message","") or "").strip().lower()
        if not body:
            body = (request.get_data(as_text=True) or "").lower()
        print(f"[RECU] {body}")

        if "terre" in body or "sol" in body:
            reply = "Test terre BEPC: Rouge caillou Alibori Kandi = tres bonne. Blanche dure = cendre/coquilles 500kg/ha."
        elif "achet" in body or "semence" in body or "engrais" in body:
            reply = "Acheter: Violet Galmi 50t/ha INRAB Ina 20k F/kg CcPA."
        elif "aide" in body or "atda" in body:
            reply = "Aide: CeCPA chaque commune + ATDA1 Kandi ATDA2 Parakou ATDA3 Natitingou."
        elif "eau" in body:
            reply = "Eau: PNDIrr SolMA goutte-a-goutte kit 500m2 filtre+vannes+tuyaux."
        elif "argent" in body or "cout" in body or "gagn" in body:
            reply = "Argent: 1ha 1 148 000F -> 35t x 500F = 17,5M benef 16,3M. Location 100-200k/ha."
        elif "bonjour" in body or "hi" in body or body == "":
            reply = "Bienvenue Nounkoun BEPC 0 import 100 ans! Envoie: TERRE, ACHETER, AIDE, EAU, ARGENT"
        else:
            reply = f"Nounkoun 0 import. Tu as dit: {body}. Envoie TERRE ACHETER AIDE EAU ARGENT."

        if "twilio" in request.path.lower() or request.values.get("From"):
            twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{reply}</Message></Response>'
            return Response(twiml, mimetype="text/xml")
        
        if request.is_json:
            print(f"[META POST] {request.get_json()}")

        return reply, 200
    except Exception as e:
        print(f"Erreur {e}")
        return "Bienvenue Nounkoun BEPC. Envoie TERRE ACHETER AIDE EAU ARGENT", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
