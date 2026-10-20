"""Tests simples pour la logique de recommandation et l'authentification.

Lancer avec : pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.recommandation import recommander_stations
from utils.auth import hash_password, seed_default_accounts, verify_login


def test_recommandation_retourne_les_5_stations():
    resultats = recommander_stations(besoin_accessibilite=False)
    assert len(resultats) == 5


def test_recommandation_filtre_par_ligne():
    resultats = recommander_stations(besoin_accessibilite=False, ligne_preferee="Ligne C")
    assert set(resultats["station"]) == {"Aéroport"}


def test_besoin_accessibilite_marque_les_bonnes_stations():
    resultats = recommander_stations(besoin_accessibilite=True)
    recommandees = resultats[resultats["recommandee"]]
    assert set(recommandees["niveau_accessibilite"]).issubset({"Bon", "Excellent"})


def test_hash_password_est_deterministe_et_non_reversible():
    h1 = hash_password("Admin123!")
    h2 = hash_password("Admin123!")
    assert h1 == h2
    assert h1 != "Admin123!"


def test_login_comptes_demo():
    seed_default_accounts()
    assert verify_login("admin", "Admin123!") == "admin"
    assert verify_login("usager", "Usager123!") == "user"
    assert verify_login("admin", "mauvais_mot_de_passe") is None
    assert verify_login("inconnu", "peu importe") is None
