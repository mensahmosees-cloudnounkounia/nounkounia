# -*- coding: utf-8 -*-
import os
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from nounkoun import traiter_message

app = Flask(__name__)

# Nécessaires pour envoyer les alertes communauté (le webhook Twilio ne peut
# répondre qu'AU paysan qui a écrit ; pour prévenir SES VOISINS, il faut un
# appel sortant via l'API Twilio, donc les identifiants de compte).
TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM")  # ex: "whatsapp:+14155238886"

_client = Client(TWILIO_SID, TWILIO_TOKEN) if TWILIO_SID and TWILIO_TOKEN else None


def _envoyer_alertes(destinataires, message):
    if not _client:
        print(f"[TWILIO NON CONFIGURÉ] {len(destinataires)} alerte(s) non envoyée(s) : {message}")
        return
    for numero in destinataires:
        try:
            _client.messages.create(from_=TWILIO_WHATSAPP_FROM, to=numero, body=message)
        except Exception as e:
            print(f"Échec envoi alerte à {numero}: {e}")


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    message = request.values.get("Body", "")
    numero = request.values.get("From", "")
    media_url = request.values.get("MediaUrl0")
    media_type = request.values.get("MediaContentType0", "")

    resultat = traiter_message(
        message, numero,
        media_url=media_url if media_url and "image" in media_type else None,
    )

    if resultat["alerte"]:
        _envoyer_alertes(resultat["alerte"]["destinataires"], resultat["alerte"]["message"])

    resp = MessagingResponse()
    resp.message(resultat["texte"])
    return str(resp)


@app.route("/health", methods=["GET"])
def health():
    return "Nounkoun OK"


if __name__ == "__main__":
    app.run(port=5000)
