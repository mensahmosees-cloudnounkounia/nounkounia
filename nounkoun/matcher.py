# -*- coding: utf-8 -*-
"""
matcher.py — Reconnaissance de la culture évoquée dans un message.

Corrige deux problèmes des versions précédentes :
1. `"mais" in message` matchait aussi "franç**ais**" ou "j**amais**" → on
   matche maintenant sur des mots entiers (frontières de mots), pas des
   sous-chaînes.
2. Les caractères spéciaux du Fon (ɔ, è, ɛ...) et les accents empêchaient
   parfois le match si l'utilisateur tapait sans accents sur son téléphone
   → on normalise (minuscules + suppression des accents) des deux côtés
   avant de comparer.
"""
import re
import unicodedata
from .data import CULTURES


def normaliser(texte: str) -> str:
    """minuscules + accents retirés (ex: 'Tè Vɔvɔ' -> 'te vovo')"""
    texte = texte.lower().strip()
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    # les caractères Fon comme ɔ/ɛ n'ont pas toujours de forme décomposée ;
    # on les ramène à leur équivalent latin le plus proche.
    texte = texte.replace("ɔ", "o").replace("ɛ", "e")
    return texte


def _construire_index():
    """
    Construit un index {nom_normalisé: id_culture}, trié plus tard par
    longueur décroissante pour que les noms composés ("igname eau") soient
    testés avant les noms simples ("igname").
    """
    index = {}
    for culture_id, data in CULTURES.items():
        candidats = [culture_id]
        candidats += list(data.get("noms", {}).values())
        candidats += data.get("alias", [])
        for var_nom, var_data in data.get("varietes", {}).items():
            candidats.append(var_nom)
        for c in candidats:
            if c:
                index[normaliser(c)] = culture_id
    return index


_INDEX = _construire_index()
# du plus long au plus court pour prioriser les correspondances précises
_NOMS_TRIES = sorted(_INDEX.keys(), key=len, reverse=True)


def trouver_culture(message: str):
    """
    Retourne (culture_id, data) si une culture est reconnue dans le message,
    sinon (None, None). Matching par mots entiers pour éviter les faux
    positifs (ex: 'français' ne doit pas déclencher 'maïs').
    """
    message_norm = normaliser(message)
    for nom in _NOMS_TRIES:
        # \b ne fonctionne pas bien avec les espaces internes des noms
        # composés, donc on construit une regex sûre pour les deux cas.
        motif = r"(?<![a-z0-9])" + re.escape(nom) + r"(?![a-z0-9])"
        if re.search(motif, message_norm):
            culture_id = _INDEX[nom]
            return culture_id, CULTURES[culture_id]
    return None, None


def lister_cultures_connues():
    """Pour les messages d'aide : liste dynamique, jamais à mettre à jour à la main."""
    noms = []
    for data in CULTURES.values():
        noms.append(data["noms"].get("fon") or data["noms"]["francais"])
    return noms
