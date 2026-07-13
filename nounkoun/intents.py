# -*- coding: utf-8 -*-
"""
intents.py — Comprend CE QUE l'utilisateur demande à propos d'une culture
déjà identifiée par matcher.py : le prix, le calendrier lunaire, une
recette de transformation, un problème (ravageur/maladie), ou une fiche
générale.

Séparer "quelle culture ?" (matcher.py) de "quelle question ?" (ici) rend
chaque ajout futur (v5, v6...) indépendant : ajouter une nouvelle intention
ne touche pas au matching des cultures, et vice versa.
"""
from .matcher import normaliser

MOTS_PRIX = ["prix", "combien", "marche", "marché", "vendre", "acheter"]
MOTS_CALENDRIER = ["quand", "planter", "semer", "lune", "calendrier", "periode"]
MOTS_RECETTE = ["recette", "comment faire", "preparer", "préparer", "transformer"]

MOTS_PROBLEME = {
    "insecte": ["mange", "mangé", "trou", "chenille", "insecte", "bete", "bête", "cochenille"],
    "carence_maladie": ["jaune", "mosaique", "mosaïque", "marbre", "marbré", "maladie"],
    "eau": ["pourri", "pourriture", "trop d'eau", "inonde", "inondé"],
    "secheresse": ["sec", "seche", "sèche", "secheresse", "sécheresse"],
}


def detecter_intention(message: str) -> str:
    """Retourne : 'prix' | 'calendrier' | 'recette' | 'probleme' | 'general'."""
    m = normaliser(message)

    if any(mot in m for mot in MOTS_PRIX):
        return "prix"
    if any(mot in m for mot in MOTS_CALENDRIER):
        return "calendrier"
    if any(mot in m for mot in MOTS_RECETTE):
        return "recette"
    for _, mots in MOTS_PROBLEME.items():
        if any(mot in m for mot in mots):
            return "probleme"
    return "general"


def detecter_type_probleme(message: str):
    """Retourne la catégorie de problème détectée, ou None."""
    m = normaliser(message)
    for categorie, mots in MOTS_PROBLEME.items():
        if any(mot in m for mot in mots):
            return categorie
    return None
