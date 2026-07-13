# -*- coding: utf-8 -*-
"""
db.py — Persistance SQLite pour les paysans et les alertes.

Remplace le `USERS_DB = {}` en mémoire de votre V6 : un dict Python vit dans
la RAM d'UN SEUL processus. Dès que Flask tourne avec plusieurs workers
(gunicorn -w 4, obligatoire en production pour tenir la charge), chaque
worker a SON PROPRE dict → un paysan enregistré par le worker 1 est invisible
pour le worker 2. Et au moindre redéploiement, tout est perdu.

SQLite règle ça : un seul fichier partagé sur disque, aucune dépendance
externe à installer/gérer. Le jour où le volume grossit vraiment
(des milliers de paysans actifs), on migre vers PostgreSQL sans changer
l'API de ce module — seules les fonctions ci-dessous changeraient
d'implémentation.
"""
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "nounkoun.db"


@contextmanager
def _connexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def initialiser():
    with _connexion() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS paysans (
                numero TEXT PRIMARY KEY,
                nom TEXT,
                commune TEXT,
                lat REAL,
                lon REAL,
                date_inscription TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alertes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_emetteur TEXT,
                culture TEXT,
                probleme TEXT,
                commune TEXT,
                date TEXT
            )
        """)


def enregistrer_paysan(numero: str, commune: str, lat: float, lon: float, nom: str = None):
    with _connexion() as conn:
        conn.execute(
            """INSERT INTO paysans (numero, nom, commune, lat, lon, date_inscription)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(numero) DO UPDATE SET
                 nom=excluded.nom, commune=excluded.commune,
                 lat=excluded.lat, lon=excluded.lon""",
            (numero, nom or "Paysan", commune, lat, lon, datetime.now().isoformat()),
        )


def obtenir_paysan(numero: str):
    with _connexion() as conn:
        row = conn.execute("SELECT * FROM paysans WHERE numero = ?", (numero,)).fetchone()
        return dict(row) if row else None


def tous_les_paysans(exclure_numero: str = None):
    with _connexion() as conn:
        if exclure_numero:
            rows = conn.execute("SELECT * FROM paysans WHERE numero != ?", (exclure_numero,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM paysans").fetchall()
        return [dict(r) for r in rows]


def enregistrer_alerte(numero_emetteur: str, culture: str, probleme: str, commune: str):
    with _connexion() as conn:
        conn.execute(
            "INSERT INTO alertes (numero_emetteur, culture, probleme, commune, date) VALUES (?, ?, ?, ?, ?)",
            (numero_emetteur, culture, probleme, commune, datetime.now().isoformat()),
        )


initialiser()
