"""
Accès à la base de données SQLite de l'application MobiliSmart.

La base (data/app.db) contient :
- les données métier nettoyées (stations, lignes, accessibilite, usagers,
  incidents, affluence agrégée) reprises de la Partie 2 du mémoire
- une table "utilisateurs" pour l'authentification (comptes de démonstration)
- une table "journal_acces" : un journal minimal des connexions, utile pour
  la conformité RGPD (traçabilité des accès, sans donnée personnelle sensible)
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "app.db"


def get_connection():
    """Ouvre une connexion à la base SQLite."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_users_table():
    """Crée la table des utilisateurs et des accès si elles n'existent pas."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
            date_creation TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS journal_acces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            date_heure TEXT NOT NULL,
            action TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def log_access(username: str, role: str, action: str):
    """Enregistre une connexion/déconnexion dans le journal d'accès.

    RGPD : seules des informations techniques minimales sont conservées
    (identifiant, rôle, horodatage, action) — aucune donnée personnelle
    sensible n'est journalisée.
    """
    conn = get_connection()
    conn.execute(
        "INSERT INTO journal_acces (username, role, date_heure, action) VALUES (?, ?, ?, ?)",
        (username, role, datetime.now().isoformat(timespec="seconds"), action),
    )
    conn.commit()
    conn.close()


def get_recent_access(limit: int = 20):
    """Retourne les derniers accès enregistrés (pour la page Administration)."""
    import pandas as pd
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT date_heure, username, role, action FROM journal_acces "
        "ORDER BY date_heure DESC LIMIT ?",
        conn, params=(limit,),
    )
    conn.close()
    return df


def table_exists(table_name: str) -> bool:
    conn = get_connection()
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    )
    exists = cur.fetchone() is not None
    conn.close()
    return exists
