"""
Script de préparation de la base data/app.db à partir du fichier Excel
fourni par l'école. A lancer une seule fois (ou à chaque mise à jour des
données sources) : `python utils/build_database.py`.

Reprend le nettoyage déjà effectué en Partie 2 du mémoire (stations hors
référentiel écartées de l'accessibilité) et ajoute une table d'affluence
agrégée (plus légère que les ~26 000 lignes brutes) pour l'Administration.
"""

import sqlite3
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.database import DB_PATH  # noqa: E402

SOURCE_XLSX = Path(__file__).resolve().parent.parent.parent.parent / "mobility_plus_datasets.xlsx"
STATIONS_VALIDES = ["Gare Centrale", "Hôpital", "Université", "Centre Ville", "Aéroport"]


def build():
    frequentation = pd.read_excel(SOURCE_XLSX, sheet_name="Frequentation_2026")
    incidents = pd.read_excel(SOURCE_XLSX, sheet_name="Incidents_2026")
    usagers = pd.read_excel(SOURCE_XLSX, sheet_name="Usagers")
    accessibilite_brute = pd.read_excel(SOURCE_XLSX, sheet_name="Accessibilite")
    referentiel_stations = pd.read_excel(SOURCE_XLSX, sheet_name="Referentiel_Stations")
    referentiel_lignes = pd.read_excel(SOURCE_XLSX, sheet_name="Referentiel_Lignes")

    stations = (
        referentiel_stations.drop_duplicates(subset="station")
        [["station", "zone", "latitude", "longitude", "capacite_max"]]
        .reset_index(drop=True)
    )
    station_ligne = referentiel_stations[["station", "ligne"]].reset_index(drop=True)
    accessibilite = accessibilite_brute[
        accessibilite_brute["station"].isin(STATIONS_VALIDES)
    ].reset_index(drop=True)

    usagers = usagers.copy()
    usagers["age_profil_coherent"] = ~(
        (usagers["profil"] == "Étudiant") & (usagers["age"] > 30)
    )

    # Fréquentation agrégée (station x ligne x jour_semaine x plage_horaire)
    # -> beaucoup plus légère que les 26 000 lignes brutes, suffisante pour
    # les graphiques de l'Administration.
    frequentation_agg = (
        frequentation.groupby(["station", "ligne", "jour_semaine", "plage_horaire"])
        .agg(taux_occupation_moyen=("taux_occupation", "mean"), nb_mesures=("taux_occupation", "count"))
        .reset_index()
    )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    stations.to_sql("stations", conn, if_exists="replace", index=False)
    station_ligne.to_sql("station_ligne", conn, if_exists="replace", index=False)
    referentiel_lignes.to_sql("lignes", conn, if_exists="replace", index=False)
    accessibilite.to_sql("accessibilite", conn, if_exists="replace", index=False)
    usagers.to_sql("usagers", conn, if_exists="replace", index=False)
    incidents.to_sql("incidents", conn, if_exists="replace", index=False)
    frequentation_agg.to_sql("frequentation_agg", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print(f"Base créée : {DB_PATH}")


if __name__ == "__main__":
    build()
