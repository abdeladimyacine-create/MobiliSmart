"""Page Prédiction d'affluence — répond au Besoin n°2 du cahier des charges."""

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "modele_affluence.pkl"

STATIONS = ["Gare Centrale", "Hôpital", "Université", "Centre Ville", "Aéroport"]
LIGNES = ["Ligne A", "Ligne B", "Ligne C"]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
PLAGES = [
    "Nuit", "Matinée", "Heure de pointe matin", "Midi",
    "Après-midi", "Heure de pointe soir", "Soirée",
]
MOIS = [str(m) for m in range(1, 13)]

COULEUR_NIVEAU = {"Faible": "🟢", "Moyenne": "🟠", "Élevée": "🔴"}


@st.cache_resource
def charger_modele():
    return joblib.load(MODEL_PATH)


st.title("📈 Prédiction d'affluence")
st.caption("Besoin n°2 — Anticiper les pics d'affluence pour fluidifier le service")

modele = charger_modele()

with st.form("formulaire_prediction"):
    col1, col2 = st.columns(2)
    with col1:
        station = st.selectbox("Station", STATIONS)
        ligne = st.selectbox("Ligne", LIGNES)
    with col2:
        jour = st.selectbox("Jour de la semaine", JOURS)
        plage = st.selectbox("Plage horaire", PLAGES)
    mois = st.select_slider("Mois", options=MOIS, value="6")

    valider = st.form_submit_button("Prédire l'affluence", type="primary")

if valider:
    entree = pd.DataFrame([{
        "station": station,
        "ligne": ligne,
        "jour_semaine": jour,
        "plage_horaire": plage,
        "mois": mois,
    }])

    prediction = modele.predict(entree)[0]
    probabilites = modele.predict_proba(entree)[0]
    proba_par_classe = dict(zip(modele.classes_, probabilites))

    st.divider()
    st.subheader(f"{COULEUR_NIVEAU.get(prediction, '')} Affluence prévue : **{prediction}**")

    df_proba = pd.DataFrame({
        "Niveau": list(proba_par_classe.keys()),
        "Probabilité": list(proba_par_classe.values()),
    }).set_index("Niveau").loc[["Faible", "Moyenne", "Élevée"]]
    st.bar_chart(df_proba)

    st.caption(
        "Modèle entraîné sur les données historiques Janvier-Juin 2026 "
        "(voir le notebook MobiliSmart_ML pour le détail de l'entraînement "
        "et la comparaison des modèles)."
    )
