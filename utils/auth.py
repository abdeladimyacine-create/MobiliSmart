"""
Authentification simple pour MobiliSmart.

Approche volontairement légère (cohérente avec le profil data/BI du porteur
de projet, cf. Partie 1.8 du mémoire) : mots de passe hachés avec SHA-256,
stockés en base SQLite, pas de dépendance externe lourde. Deux comptes de
démonstration sont créés automatiquement au premier lancement.

RGPD : aucune donnée personnelle réelle n'est demandée à l'inscription —
seuls un identifiant, un mot de passe (haché, jamais stocké en clair) et
un rôle sont conservés.
"""

import hashlib
from datetime import datetime

from utils.database import get_connection, init_users_table


def hash_password(password: str) -> str:
    """Hache un mot de passe avec SHA-256 (suffisant pour ce prototype)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def seed_default_accounts():
    """Crée les comptes de démonstration s'ils n'existent pas encore."""
    init_users_table()
    conn = get_connection()
    existing = conn.execute("SELECT COUNT(*) FROM utilisateurs").fetchone()[0]
    if existing == 0:
        comptes_demo = [
            ("admin", hash_password("Admin123!"), "admin"),
            ("usager", hash_password("Usager123!"), "user"),
        ]
        for username, pwd_hash, role in comptes_demo:
            conn.execute(
                "INSERT INTO utilisateurs (username, password_hash, role, date_creation) "
                "VALUES (?, ?, ?, ?)",
                (username, pwd_hash, role, datetime.now().isoformat(timespec="seconds")),
            )
        conn.commit()
    conn.close()


def verify_login(username: str, password: str):
    """Vérifie les identifiants. Retourne le rôle ('admin'/'user') si valide, sinon None."""
    conn = get_connection()
    row = conn.execute(
        "SELECT password_hash, role FROM utilisateurs WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()

    if row is None:
        return None

    password_hash, role = row
    if password_hash == hash_password(password):
        return role
    return None
