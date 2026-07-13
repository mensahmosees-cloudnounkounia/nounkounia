# -*- coding: utf-8 -*-
"""
diagnostic.py — Diagnostic à partir d'une DESCRIPTION TEXTE des symptômes.

Note importante sur le nommage : votre V6 appelait ceci "IA Vision" et
affichait un "% de confiance" (`diag = confiance * 30, max 95%`). Je le
renomme volontairement en "diagnostic par description" et je supprime le
faux pourcentage de confiance, pour deux raisons :

1. Ce n'est PAS de la vision par ordinateur — la photo n'est jamais
   analysée, seul le texte tapé par le paysan l'est. Lui faire croire
   qu'une IA a "vu" sa photo, alors qu'on lui redemande en fait de la
   décrire à l'écrit, casse la confiance dès qu'il s'en rend compte.
2. Un "95% sûr" calculé comme `nombre_de_mots_trouvés * 30` n'a aucune
   valeur statistique réelle. Afficher un chiffre précis pour un simple
   comptage de mots-clés est trompeur — un paysan pourrait traiter sa
   parcelle sur la foi d'un chiffre qui ne veut rien dire.

Si vous voulez un vrai diagnostic par photo plus tard (Gemini Vision /
GPT-4V), ce module sera le bon endroit pour brancher l'appel API — la
fonction `diagnostiquer_par_description` restera le filet de sécurité
quand l'utilisateur n'a pas de photo ou une image de mauvaise qualité.
"""
from .matcher import normaliser
from .data import SIGNES_VISUELS, CULTURES


def diagnostiquer_par_description(culture_id: str, description: str):
    """
    Retourne (probleme, mots_trouves) le plus probable d'après les mots-clés
    de la description, ou (None, []) si rien ne correspond.
    """
    tags_culture = SIGNES_VISUELS.get(culture_id, {})
    desc = normaliser(description)

    meilleur_probleme, meilleurs_mots = None, []
    for probleme, tags in tags_culture.items():
        trouves = [t for t in tags if normaliser(t) in desc]
        if len(trouves) > len(meilleurs_mots):
            meilleur_probleme, meilleurs_mots = probleme, trouves

    return meilleur_probleme, meilleurs_mots


def formatter_diagnostic(culture_id: str, description: str) -> str:
    data = CULTURES.get(culture_id, {})
    nom_aff = data.get("noms", {}).get("fon") or data.get("noms", {}).get("francais", culture_id)

    probleme, mots_trouves = diagnostiquer_par_description(culture_id, description)
    if not probleme:
        return ("❌ Je n'ai pas reconnu de symptôme précis. Décris par exemple : "
                "'taches noires sur les feuilles' ou 'insectes blancs'.")

    lignes = [f"🔍 Probablement : {probleme.upper()} sur {nom_aff}"]
    lignes.append("📝 D'après : " + ", ".join(mots_trouves))

    solutions = data.get("solutions_naturelles")
    if solutions:
        lignes.append("\n✅ Solutions naturelles :")
        lignes += [f" - {s} : {d}" for s, d in solutions.items()]

    lignes.append("\n⚠️ Diagnostic basé sur ta description, pas sur la photo elle-même. "
                   "Si le problème persiste après traitement, montre la plante à un "
                   "technicien agricole de ta zone.")
    return "\n".join(lignes)
