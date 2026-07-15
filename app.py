from flask import Flask, request, send_from_directory, jsonify, Response
import pathlib, json, os

app = Flask(__name__)
BASE = pathlib.Path(__file__).parent

def load_zones():
    try:
        p = BASE/"data/benin_oignon_zonage_complet.json"
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except: pass
    return []

# --- PAGE D'ACCUEIL - NE RENVOIE JAMAIS 404 (pour Meta + Render) ---
@app.route("/", methods=["GET"])
def home():
    try:
        fp = BASE/"farmer_app/index.html"
        if fp.exists():
            return send_from_directory(BASE/"farmer_app", "index.html")
    except: pass
    # Fallback inline pour Render si farmer_app manque
    return """
    <!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Nounkounia - 0 Import 100 ans</title></head>
    <body style="font-family:system-ui;padding:20px;background:#fff8e6">
    <h1>🇧🇯 NOUNKOUNIA - Oignon Benin 0 Import 100 ans</h1>
    <p><b>Objectif:</b> Malanville <20t/ha -> 35t/ha avec Trichoderma 0.5t/ha = 3kg/planche</p>
    <p><b>Terre BEPC:</b> Rouge cailloux Kandi Malanville = bonne. Blanche dure brique = cendre/coquilles 500kg/ha</p>
    <p><b>Acheter:</b> Violet Galmi 50t/ha INRAB Ina Parakou 20k F/kg, NPK Uree depot ATDA CeCPA 242k tonnes, Trichoderma 35t/ha BioPhyto DEMA AGRO Ouidah 4000F/L</p>
    <p><b>Aide:</b> CeCPA chaque commune + ATDA1 Kandi ATDA2 Parakou ATDA3 Natitingou ATDA4 Abomey ATDA7 Ouidah</p>
    <p><b>Argent:</b> 1ha depense 1 148 000F recolte 35t x 500F = 17,5M benef 16,3M</p>
    <ul>
      <li><a href="/health">/health</a></li>
      <li><a href="/api/zones">/api/zones 8 zones Benin</a></li>
      <li><a href="/paysan">/paysan - App paysan BEPC</a></li>
      <li><a href="/webhook?Body=TERRE">/webhook?Body=TERRE - Test WhatsApp</a></li>
    </ul>
    <p>Politique confidentialite: aucune donnee personnelle collectee. Messages agricoles uniquement.</p>
    </body></html>
    """, 200

@app.route("/paysan")
def paysan():
    return """
    <html><body style="font-family:sans-serif;background:#fff8e6;padding:10px">
    <h1>🇧🇯 NOUNKOUN - Oignon Benin</h1>
    <p><b>Terre:</b> Rouge cailloux = bonne (Kandi, Malanville). Blanche dure = mets cendre/coquilles 500kg/ha</p>
    <p><b>Acheter:</b> Semences Violet Galmi 50t/ha: INRAB Ina Parakou 20k F/kg - NPK Uree depot ATDA+CeCPA 242k tonnes</p>
    <p><b>Aide:</b> CeCPA chaque commune + ATDA1 Kandi ATDA2 Parakou ATDA3 Natitingou ATDA4 Abomey ATDA7 Ouidah</p>
    <p><b>Argent:</b> 1ha depense 1 148 000F recolte 35t x 500F = 17,5M benef 16,3M</p>
    <p><b>Objectif:</b> 0 importation 100 ans - Malanville <20 -> 35t/ha avec Trichoderma</p>
    </body></html>
    """

@app.route("/data/<path:filename>")
def data_file(filename):
    try:
        return send_from_directory(BASE/"data", filename)
    except:
        return jsonify({"error":"fichier non trouve"}), 404

@app.route("/health")
def health():
    return jsonify({"status":"ok","app":"nounkounia","objectif":"0 import 100 ans","zones":len(load_zones())})

@app.route("/api/zones")
def api_zones():
    return jsonify(load_zones())

@app.route("/api/intrants")
def api_intrants():
    try:
        p = BASE/"data/acces_intrants_benin_100ans.json"
        if p.exists():
            return jsonify(json.loads(p.read_text(encoding="utf-8")))
    except: pass
    return jsonify({"objectif":"0 importation","semences":"Violet Galmi 50t/ha INRAB Ina"})

def handle_whatsapp():
    try:
        body = (request.values.get("Body","") or request.args.get("Body","") or request.args.get("message","") or "").strip().lower()
        if not body:
            body = (request.get_data(as_text=True) or "").lower()
        print(f"WhatsApp recu: {body}")
        if "terre" in body or "sol" in body:
            reply = "Test terre BEPC: Rouge cailloux Alibori Kandi = tres bonne. Blanche dure = cendre/coquilles 500kg/ha. Qui colle = planche haute. CeCPA."
        elif "achet" in body or "semence" in body or "engrais" in body:
            reply = "Acheter: Violet Galmi 50t/ha INRAB Ina 20k F/kg CeCPA. NPK Uree depot ATDA CeCPA 242k t. Trichoderma 35t/ha BioPhyto DEMA AGRO Ouidah 4000F/L."
        elif "aide" in body or "atda" in body or "cecpa" in body:
            reply = "Aide: CeCPA chaque commune + ATDA1 Kandi ATDA2 Parakou ATDA3 Natitingou ATDA4 Abomey ATDA7 Ouidah."
        elif "eau" in body:
            reply = "Eau: PNDIrr SoNaMA goutte-a-goutte kit 500m2 filtre+vannes+tuyaux. 1x/sem debut, tous 5j bulbe, arrete 1 sem avant."
        elif "argent" in body or "cout" in body or "gagn" in body:
            reply = "Argent: 1ha 1 148 000F -> 35t x 500F = 17,5M benef 16,3M. Location 100-200k/ha. Seme Nov-Jan recolte Mars-Mai."
        elif "bonjour" in body or "hi" in body or body == "":
            reply = "Bienvenue Nounkoun BEPC 0 import 100 ans! Envoie: TERRE, ACHETER, AIDE, EAU, ARGENT ou COMMUNE ex: Ze Kandi"
        else:
            reply = f"Nounkoun 0 import. Tu as dit: {body}. Envoie TERRE ACHETER AIDE EAU ARGENT."
    except Exception as e:
        print(f"Erreur: {e}")
        reply = "Bienvenue Nounkoun BEPC. Envoie TERRE ACHETER AIDE EAU ARGENT"
    # Twilio attend XML
    if "twilio" in request.path.lower() or request.values.get("From"):
        twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{reply}</Message></Response>'
        return Response(twiml, mimetype="text/xml")
    return reply, 200

@app.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and challenge:
            return challenge, 200
        return handle_whatsapp()
    return handle_whatsapp()

@app.route("/whatsapp", methods=["GET","POST"])
def whatsapp():
    return handle_whatsapp()

@app.route("/twilio/whatsapp", methods=["GET","POST"])
def twilio_whatsapp():
    return handle_whatsapp()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("="*60)
    print("NOUNKOUN V6 FIXE - 0 IMPORT 100 ANS - 0 404")
    print(f"App: http://localhost:{port}/")
    print(f"App paysan: http://localhost:{port}/paysan")
    print(f"Health: http://localhost:{port}/health")
    print(f"WhatsApp test: http://localhost:{port}/webhook?Body=TERRE")
    print("="*60)
    app.run(host="0.0.0.0", port=port, debug=False)

