"""Page Recommandation de trajet accessible — répond aux Besoins n°1 et n°4."""

import streamlit as st

from utils.recommandation import recommander_stations
from utils.database import get_connection
import pandas as pd

st.title("♿ Recommandation de trajet accessible")
st.caption("Besoins n°1 et n°4 — Visibilité de l'accessibilité, adaptée à votre profil")

conn = get_connection()
lignes_disponibles = ["Toutes les lignes"] + pd.read_sql_query(
    "SELECT nom_ligne FROM lignes", conn
)["nom_ligne"].tolist()
conn.close()

with st.form("formulaire_recommandation"):
    besoin_pmr = st.checkbox(
        "J'ai besoin d'accessibilité (PMR)",
        help="Si coché, seules les stations de niveau d'accessibilité Bon ou Excellent sont mises en avant.",
    )
    ligne_preferee = st.selectbox("Ligne préférée (optionnel)", lignes_disponibles)
    valider = st.form_submit_button("Voir les stations recommandées", type="primary")

if valider:
    resultats = recommander_stations(besoin_pmr, ligne_preferee)

    st.divider()
    for _, row in resultats.iterrows():
        badge = "✅ Recommandée" if row["recommandee"] else "—"
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['station']}** · {row['zone']}")
                equipements = []
                if row["ascenseur"]:
                    equipements.append("Ascenseur")
                if row["rampe_acces"]:
                    equipements.append("Rampe d'accès")
                if row["signaletique_adaptee"]:
                    equipements.append("Signalétique adaptée")
                st.caption(", ".join(equipements) if equipements else "Aucun équipement PMR recensé")
            with col2:
                st.metric("Score accessibilité", f"{row['score_normalise']:.0f}/100")
                st.caption(badge)

    if besoin_pmr and not resultats["recommandee"].any():
        st.warning(
            "Aucune station de niveau Bon/Excellent sur ce filtre — "
            "c'est le reflet direct du déficit d'accessibilité identifié "
            "en Partie 1.4 du mémoire, pas un bug de l'application.",
            icon="⚠️",
        )
