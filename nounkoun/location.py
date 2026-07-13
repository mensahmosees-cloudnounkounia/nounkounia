# -*- coding: utf-8 -*-
"""
location.py — Enregistrement GPS d'un paysan + recherche de voisins.

Note : la distance est calculée avec la formule de haversine, codée à la
main plutôt que d'ajouter la dépendance `geopy` juste pour ça — un calcul
de distance à vol d'oiseau n'a pas besoin d'une librairie externe.
"""
import math
from .communes import trouver_commune, lister_communes_connues
from . import db


def enregistrer_paysan_gps(numero: str, texte_commune: str, nom: str = None) -> str:
    nom_commune, gps = trouver_commune(texte_commune)
    if not gps:
        return ("❌ Commune non reconnue. Essaie : " + ", ".join(lister_communes_connues()[:8]) + "...")
    db.enregistrer_paysan(numero, nom_commune, gps[0], gps[1], nom)
    return (f"📍 Position enregistrée : {nom_commune}\n"
            f"Tu recevras les alertes météo et maladies de ta zone.")


def _distance_km(gps1, gps2) -> float:
    """Distance à vol d'oiseau (formule de haversine)."""
    lat1, lon1 = gps1
    lat2, lon2 = gps2
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def trouver_paysans_proches(numero: str, rayon_km: float = 10):
    moi = db.obtenir_paysan(numero)
    if not moi:
        return None  # pas encore enregistré
    proches = []
    for p in db.tous_les_paysans(exclure_numero=numero):
        d = _distance_km((moi["lat"], moi["lon"]), (p["lat"], p["lon"]))
        if d <= rayon_km:
            proches.append({**p, "distance_km": round(d, 1)})
    return sorted(proches, key=lambda x: x["distance_km"])
