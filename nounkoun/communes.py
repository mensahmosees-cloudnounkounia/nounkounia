# -*- coding: utf-8 -*-
"""
communes.py — Coordonnées GPS des communes du Bénin les plus citées.

Pourquoi une table statique plutôt qu'un géocodage en ligne (Nominatim) à
chaque message ?
1. Nominatim a une limite de 1 requête/seconde et bloque les gros volumes —
   inutilisable en direct dans un webhook qui doit répondre vite.
2. Les communes du Bénin ne changent pas : autant les figer une fois pour
   toutes et ajouter les manquantes au besoin.
3. Zéro dépendance réseau supplémentaire = zéro nouveau point de panne.

Pour ajouter une commune : une ligne ici, rien d'autre à changer.
"""
from .matcher import normaliser

COMMUNES_GPS = {
    "Zè": (6.784, 2.298),
    "Allada": (6.667, 2.150),
    "Toffo": (6.842, 2.117),
    "Savalou": (7.928, 1.975),
    "Djougou": (9.708, 1.666),
    "Dassa-Zoumè": (7.750, 2.183),
    "Glazoué": (7.983, 2.350),
    "Pobè": (6.983, 2.666),
    "Kétou": (7.359, 2.602),
    "Abomey": (7.183, 1.983),
    "Bohicon": (7.178, 2.067),
    "Banikoara": (11.297, 2.438),
    "Kandi": (11.134, 2.938),
    "Parakou": (9.337, 2.630),
    "Bembèrèkè": (10.228, 2.665),
    "Malanville": (11.867, 3.383),
    "Karimama": (12.067, 3.200),
    "Natitingou": (10.317, 1.383),
    "Porto-Novo": (6.497, 2.605),
    "Lokossa": (6.639, 1.717),
    "Cotonou": (6.367, 2.433),
}

_INDEX_NORMALISE = {normaliser(nom): (nom, gps) for nom, gps in COMMUNES_GPS.items()}


def trouver_commune(texte: str):
    """Retourne (nom_officiel, (lat, lon)) si la commune est reconnue, sinon (None, None)."""
    t = normaliser(texte)
    for nom_norm, (nom_officiel, gps) in _INDEX_NORMALISE.items():
        if nom_norm in t:
            return nom_officiel, gps
    return None, None


def lister_communes_connues():
    return sorted(COMMUNES_GPS.keys())
