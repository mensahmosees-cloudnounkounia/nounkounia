# -*- coding: utf-8 -*-
"""
community.py — Alertes entre paysans proches.

Important : ce module ne fait PAS l'envoi WhatsApp lui-même. Il calcule
QUI doit être prévenu et QUOI leur dire, et retourne cette liste à
l'appelant (app.py). C'est app.py — qui a accès au client Twilio — qui
envoie réellement les messages. Séparer "décider qui prévenir" de
"envoyer le message" permet de tester ce module sans dépendre de Twilio,
et de changer de canal d'envoi (SMS, Telegram...) sans toucher à cette
logique.
"""
from . import db
from .location import trouver_paysans_proches

RAYON_ALERTE_KM = 15
MAX_DESTINATAIRES = 5  # éviter le spam


def preparer_alerte(numero_emetteur: str, culture_id: str, nom_culture: str, probleme: str):
    """
    Retourne un dict :
      {"envoyee": bool, "destinataires": [...], "message": "...", "resume": "..."}
    `destinataires` contient les numéros à qui app.py doit envoyer `message`.
    """
    emetteur = db.obtenir_paysan(numero_emetteur)
    if not emetteur:
        return {"envoyee": False, "destinataires": [], "message": "",
                "resume": "Enregistre ta position d'abord : 'je suis à Zè'"}

    proches = trouver_paysans_proches(numero_emetteur, rayon_km=RAYON_ALERTE_KM)
    db.enregistrer_alerte(numero_emetteur, culture_id, probleme, emetteur["commune"])

    if not proches:
        return {"envoyee": False, "destinataires": [], "message": "",
                "resume": "✅ Aucun paysan enregistré à proximité pour l'instant. "
                          "Tu es la première sentinelle de ta zone !"}

    destinataires = [p["numero"] for p in proches[:MAX_DESTINATAIRES]]
    message = (f"🚨 ALERTE {emetteur['commune']}\n"
               f"{emetteur['nom']} signale : {probleme} sur {nom_culture}\n"
               f"Vérifie tes champs et traite en préventif si besoin.")

    resume = f"📡 Alerte préparée pour {len(destinataires)} paysan(s) proche(s) :\n"
    resume += "\n".join(f"• {p['nom']} à {p['distance_km']}km ({p['commune']})" for p in proches[:MAX_DESTINATAIRES])

    return {"envoyee": True, "destinataires": destinataires, "message": message, "resume": resume}


def lister_voisins(numero: str):
    proches = trouver_paysans_proches(numero, rayon_km=10)
    if proches is None:
        return "📍 Enregistre ta position d'abord : 'je suis à Zè'"
    if not proches:
        return "Aucun paysan enregistré à moins de 10km pour l'instant."
    lignes = ["👥 PAYSANS PROCHES (10km) :"]
    lignes += [f"• {p['nom']} - {p['commune']} ({p['distance_km']}km)" for p in proches]
    return "\n".join(lignes)
