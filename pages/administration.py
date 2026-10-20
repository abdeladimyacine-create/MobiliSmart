"""Page Administration — réservée au rôle admin. Répond au Besoin n°3
(outil de pilotage transverse) et au critère 6 de la grille (pilotage/gestion)."""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from utils.database import get_connection, get_recent_access

if st.session_state.get("role") != "admin":
    st.error("Accès réservé aux administrateurs.")
    st.stop()

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "modele_affluence.pkl"

st.title("⚙️ Administration")
st.caption("Besoin n°3 — Outil de pilotage transverse, réservé au rôle administrateur")

onglet_stats, onglet_modele, onglet_journal = st.tabs(
    ["Statistiques", "Paramétrage du modèle", "Journal d'accès"]
)

# ---------------------------------------------------------------- Statistiques
with onglet_stats:
    conn = get_connection()
    frequentation_agg = pd.read_sql_query("SELECT * FROM frequentation_agg", conn)
    incidents = pd.read_sql_query("SELECT * FROM incidents", conn)
    usagers = pd.read_sql_query("SELECT * FROM usagers", conn)
    accessibilite = pd.read_sql_query("SELECT * FROM accessibilite", conn)
    conn.close()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Usagers suivis", len(usagers))
    col2.metric("Incidents enregistrés", len(incidents))
    pct_affluence = (incidents["type_incident"] == "Affluence excessive").mean() * 100
    col3.metric("% incidents liés à l'affluence", f"{pct_affluence:.1f} %")
    col4.metric("Score accessibilité moyen", f"{accessibilite['score_normalise'].mean():.0f}/100")

    st.subheader("Taux d'occupation moyen par station")
    st.bar_chart(
        frequentation_agg.groupby("station")["taux_occupation_moyen"].mean().sort_values(ascending=False)
    )

    st.subheader("Incidents par ligne et par type")
    croisement = incidents.groupby(["ligne", "type_incident"]).size().unstack(fill_value=0)
    st.bar_chart(croisement)

    st.subheader("Satisfaction moyenne par profil usager")
    st.bar_chart(usagers.groupby("profil")["satisfaction"].mean().sort_values())

# ---------------------------------------------------------------- Modèle
with onglet_modele:
    modele = joblib.load(MODEL_PATH)
    classifieur = modele.named_steps["model"]

    st.subheader("Modèle actuellement en production")
    st.write(f"**Type de modèle :** {type(classifieur).__name__}")

    st.write("**Hyperparamètres :**")
    st.json(classifieur.get_params())

    st.write("**Classes prédites :**", ", ".join(classifieur.classes_))

    st.info(
        "Pour changer de modèle, ré-exécuter le notebook MobiliSmart_ML.ipynb "
        "(section 7-9) puis remplacer models/modele_affluence.pkl. "
        "Ce choix reste manuel et documenté, volontairement : un ré-entraînement "
        "automatique en production sortirait du périmètre de ce prototype (cf. 1.8 du mémoire).",
        icon="ℹ️",
    )

# ---------------------------------------------------------------- Journal
with onglet_journal:
    st.subheader("Derniers accès à l'application")
    st.caption(
        "Journal minimal à but de traçabilité (RGPD) — identifiant, rôle "
        "et horodatage uniquement, aucune donnée personnelle sensible."
    )
    journal = get_recent_access(limit=50)
    st.dataframe(journal, use_container_width=True, hide_index=True)
