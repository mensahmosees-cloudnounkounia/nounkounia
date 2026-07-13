# -*- coding: utf-8 -*-
"""
dispatcher.py — Point d'entrée V6, appelé par app.py.

Route un message WhatsApp vers le bon traitement :
  1. Enregistrement GPS ("je suis à Zè")
  2. Photo reçue (on ne l'analyse pas : voir diagnostic.py, on demande une
     description)
  3. Description de symptôme -> diagnostic + proposition d'alerte communauté
  4. "voisins" / "paysans proches" -> liste des paysans à proximité
  5. Sinon -> comportement V1-V5 inchangé (responder.repondre)

Retourne toujours un dict :
  {"texte": str, "alerte": None | {"destinataires": [...], "message": str}}
app.py envoie `texte` au paysan, et si `alerte` n'est pas None, envoie en
plus `alerte["message"]` à chaque numéro de `alerte["destinataires"]`.
"""
import re
from .matcher import normaliser, trouver_culture
from .location import enregistrer_paysan_gps
from .diagnostic import formatter_diagnostic, diagnostiquer_par_description
from .community import preparer_alerte, lister_voisins
from .responder import repondre as repondre_standard

MOTS_GPS = ["je suis a ", "je suis à "]
MOTS_SYMPTOME = ["taches", "jaune", "trous", "blanc", "noir", "marbre", "insecte", "cochenille", "pourri"]
MOTS_VOISINS = ["voisins", "paysans proches"]


def _sans_alerte(texte: str) -> dict:
    return {"texte": texte, "alerte": None}


def traiter_message(message: str, numero: str, media_url: str = None) -> dict:
    message = message or ""
    m = normaliser(message)

    # 1. Enregistrement GPS
    for cle in MOTS_GPS:
        if cle in m:
            # on ne retire que la préposition en TÊTE de chaîne ("à "/"a "),
            # jamais à l'intérieur du nom (sinon "à Allada" -> "llada")
            reste = message.lower().split("je suis", 1)[-1].strip()
            reste = re.sub(r"^(à|a)\s+", "", reste)
            return _sans_alerte(enregistrer_paysan_gps(numero, reste.strip()))

    # 2. Photo reçue : pas d'analyse d'image réelle, on guide vers la description
    if media_url:
        culture_id, data = trouver_culture(message)
        if culture_id:
            nom_aff = data["noms"].get("fon") or data["noms"]["francais"]
            return _sans_alerte(
                f"📸 Photo {nom_aff} reçue. Décris ce que tu vois pour que je t'aide :\n"
                f"- Taches noires / feuilles jaunes / trous ?\n"
                f"- Insectes blancs ou verts ?\n"
                f"- Tubercule déformé ?"
            )
        return _sans_alerte("📸 Photo reçue. Dis-moi aussi de quelle culture il s'agit "
                             "(ex : 'photo tè', 'photo agbeli').")

    # 3. Voisins / communauté
    if any(mot in m for mot in MOTS_VOISINS):
        return _sans_alerte(lister_voisins(numero))

    # 4. Description de symptôme -> diagnostic + alerte
    if any(mot in m for mot in MOTS_SYMPTOME):
        culture_id, data = trouver_culture(message)
        if culture_id:
            texte_diag = formatter_diagnostic(culture_id, message)
            probleme, _ = diagnostiquer_par_description(culture_id, message)
            if probleme:
                nom_aff = data["noms"].get("fon") or data["noms"]["francais"]
                alerte = preparer_alerte(numero, culture_id, nom_aff, probleme)
                texte_final = texte_diag + "\n\n" + alerte["resume"]
                if alerte["envoyee"]:
                    return {"texte": texte_final,
                            "alerte": {"destinataires": alerte["destinataires"], "message": alerte["message"]}}
                return _sans_alerte(texte_final)
            return _sans_alerte(texte_diag)

    # 5. Comportement standard (V1-V5) : prix / calendrier / recette / fiche culture
    return _sans_alerte(repondre_standard(message))
