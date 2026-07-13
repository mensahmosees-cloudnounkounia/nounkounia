# -*- coding: utf-8 -*-
"""
responder.py — Assemble la réponse texte envoyée au paysan, à partir de :
  - la culture reconnue (matcher.py)
  - l'intention détectée (intents.py)

repondre(message) est LE point d'entrée unique utilisé par app.py.
"""
from .matcher import trouver_culture, lister_cultures_connues
from .intents import detecter_intention, detecter_type_probleme

MESSAGE_INCONNU = (
    "🌱 Je n'ai pas reconnu la culture. Cultures que je connais : {}.\n"
    "Tu peux aussi demander : prix, calendrier, ou recette."
)

LIBELLES_PROBLEME = {
    "insecte": "🐛 Problème détecté : insecte / chenille",
    "carence_maladie": "💛 Problème détecté : carence ou maladie (virus, mosaïque)",
    "eau": "💧 Problème détecté : excès d'eau / pourriture",
    "secheresse": "☀️ Problème détecté : manque d'eau / sécheresse",
}


def _bloc_prix(nom_aff: str, data: dict) -> str:
    prix = data.get("prix_marche")
    if not prix:
        return f"Je n'ai pas encore de prix marché pour {nom_aff}."
    lignes = [f"💰 PRIX {nom_aff.upper()} :"]
    lignes += [f"📍 {lieu} : {valeur}" for lieu, valeur in prix.items()]
    return "\n".join(lignes)


def _bloc_calendrier(nom_aff: str, data: dict) -> str:
    cal = data.get("calendrier_lunaire")
    if not cal:
        return f"Je n'ai pas encore le calendrier lunaire pour {nom_aff}. Zone : {data.get('zone', 'Bénin')}."
    lignes = [f"🌙 CALENDRIER {nom_aff.upper()} :"]
    if "plantation" in cal:
        lignes.append(f"📅 Plantation : {cal['plantation']}")
    if "recolte" in cal:
        lignes.append(f"🌾 Récolte : {cal['recolte']}")
    if "dicton" in cal:
        lignes.append(f"🗣️ {cal['dicton']}")
    if "interdit" in cal:
        lignes.append(f"⚠️ {cal['interdit']}")
    return "\n".join(lignes)


def _bloc_recette(nom_aff: str, data: dict, message: str) -> str:
    recettes = data.get("recettes_post_recolte")
    if not recettes:
        return f"Je n'ai pas encore de recette de transformation pour {nom_aff}."
    from .matcher import normaliser
    m = normaliser(message)
    for nom_recette, procede in recettes.items():
        if normaliser(nom_recette.replace("_", " ")) in m:
            return f"🍲 {nom_recette.upper()} :\n{procede}"
    # aucune recette précise nommée -> on les liste toutes
    lignes = [f"🍲 RECETTES {nom_aff.upper()} :"]
    lignes += [f"• {r}: {p}" for r, p in recettes.items()]
    return "\n".join(lignes)


def _bloc_probleme(nom_aff: str, data: dict, categorie: str) -> str:
    lignes = [LIBELLES_PROBLEME.get(categorie, "Problème détecté")]
    solutions = data.get("solutions_naturelles")
    if solutions:
        lignes.append("✅ Solutions naturelles :")
        lignes += [f" - {s} : {d}" for s, d in solutions.items()]
    else:
        lignes.append("✅ Solution générale : compost + rotation des cultures")
    return "\n".join(lignes)


def _bloc_general(nom_aff: str, data: dict) -> str:
    lignes = [f"🍠 {data['noms']['francais']} / {nom_aff}"]
    lignes.append(f"📍 Zone : {data.get('zone', 'Bénin')}")
    if data.get("cycle"):
        lignes.append(f"⏰ Cycle : {data['cycle']}")
    if data.get("varietes"):
        lignes.append("📋 Variétés :")
        for nom_var, info in list(data["varietes"].items())[:3]:
            lignes.append(f" • {nom_var} : {info.get('caractere', '')}")
    lignes.append(f"\n💰 Écris 'prix {nom_aff}' · 🌙 'quand planter {nom_aff}' · 🍲 'recette {nom_aff}'")
    return "\n".join(lignes)


def repondre(message: str) -> str:
    if not message or not message.strip():
        return MESSAGE_INCONNU.format(", ".join(lister_cultures_connues()))

    culture_id, data = trouver_culture(message)
    if not culture_id:
        return MESSAGE_INCONNU.format(", ".join(lister_cultures_connues()))

    nom_aff = data["noms"].get("fon") or data["noms"]["francais"]
    intention = detecter_intention(message)

    if intention == "prix":
        return _bloc_prix(nom_aff, data)
    if intention == "calendrier":
        return _bloc_calendrier(nom_aff, data)
    if intention == "recette":
        return _bloc_recette(nom_aff, data, message)
    if intention == "probleme":
        categorie = detecter_type_probleme(message)
        return _bloc_probleme(nom_aff, data, categorie)
    return _bloc_general(nom_aff, data)
