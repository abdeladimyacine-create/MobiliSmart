"""
Logique de recommandation de trajet accessible.

Ce n'est pas un modèle de machine learning : c'est une logique de filtrage
et de scoring sur la table "accessibilite", cohérente avec le choix fait en
Partie 2 du mémoire (profil orienté data/BI, pas de sur-ingénierie pour une
fonctionnalité qui n'en a pas besoin).
"""

import pandas as pd
from utils.database import get_connection


def recommander_stations(besoin_accessibilite: bool, ligne_preferee: str | None = None) -> pd.DataFrame:
    """Retourne les stations recommandées, triées par score d'accessibilité.

    - Si besoin_accessibilite est True, seules les stations de niveau
      "Bon" ou "Excellent" sont mises en avant.
    - Si une ligne préférée est précisée, les résultats sont filtrés sur
      les stations desservies par cette ligne.
    """
    conn = get_connection()
    stations = pd.read_sql_query("SELECT * FROM stations", conn)
    accessibilite = pd.read_sql_query("SELECT * FROM accessibilite", conn)
    station_ligne = pd.read_sql_query("SELECT * FROM station_ligne", conn)
    conn.close()

    resultat = stations.merge(accessibilite, on="station", how="left")

    if ligne_preferee and ligne_preferee != "Toutes les lignes":
        stations_de_la_ligne = station_ligne.loc[
            station_ligne["ligne"] == ligne_preferee, "station"
        ]
        resultat = resultat[resultat["station"].isin(stations_de_la_ligne)]

    resultat = resultat.sort_values("score_normalise", ascending=False).reset_index(drop=True)

    if besoin_accessibilite:
        resultat["recommandee"] = resultat["niveau_accessibilite"].isin(["Bon", "Excellent"])
    else:
        resultat["recommandee"] = True

    colonnes = [
        "station", "zone", "niveau_accessibilite", "score_normalise",
        "ascenseur", "rampe_acces", "signaletique_adaptee", "recommandee",
    ]
    return resultat[colonnes]
