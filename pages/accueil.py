"""Page d'accueil : présentation de l'application MobiliSmart."""

import streamlit as st

st.title("🚍 MobiliSmart")
st.caption("Un service intelligent d'affluence et d'accessibilité pour Mobility+")

st.markdown(
    f"Bonjour **{st.session_state.get('username', '')}** "
    f"(profil : {st.session_state.get('role', '')})."
)

st.divider()

tab_projet, tab_besoins, tab_confidentialite = st.tabs(
    ["Le projet", "Les besoins couverts", "Confidentialité"]
)

with tab_projet:
    st.subheader("Pourquoi MobiliSmart ?")
    st.write(
        "Suite à un audit interne, Mobility+ a identifié cinq problématiques : "
        "un accès difficile à ses services pour certains publics, une "
        "sous-exploitation de ses données, des interfaces peu adaptées, un "
        "manque d'outils de pilotage, et l'absence de stratégie "
        "d'accompagnement au changement."
    )
    st.write(
        "MobiliSmart répond à ces constats par trois briques complémentaires, "
        "accessibles selon votre profil : un **dashboard de pilotage** "
        "(réservé aux administrateurs), un **modèle de prédiction d'affluence**, "
        "et un **système de recommandation de trajet accessible**."
    )

with tab_besoins:
    st.subheader("Les 4 besoins identifiés en cahier des charges")
    st.markdown(
        "- **Besoin n°1** — Rendre visible l'accessibilité réelle de chaque station avant le déplacement.\n"
        "- **Besoin n°2** — Anticiper les pics d'affluence pour réduire les incidents associés.\n"
        "- **Besoin n°3** — Donner à Mobility+ un outil de pilotage transverse.\n"
        "- **Besoin n°4** — Adapter le service aux profils d'usagers les plus sensibles "
        "(PMR, actifs pendulaires, étudiants)."
    )
    st.info(
        "Les pages **Prédiction d'affluence** et **Recommandation de trajet** "
        "répondent respectivement aux besoins n°2 et n°1/n°4. "
        "La page **Administration** (réservée aux administrateurs) répond au besoin n°3.",
        icon="ℹ️",
    )

with tab_confidentialite:
    st.subheader("Confidentialité et conformité RGPD")
    st.write(
        "Ce prototype utilise un jeu de données **fictif**, fourni dans le "
        "cadre du mémoire. Si ce projet était déployé en conditions réelles :"
    )
    st.markdown(
        "- les données usagers seraient anonymisées ;\n"
        "- les mots de passe ne sont jamais stockés en clair (hachage SHA-256) ;\n"
        "- le journal d'accès ne conserve que des informations techniques "
        "minimales (identifiant, rôle, horodatage), consultable par un "
        "administrateur dans la page Administration ;\n"
        "- aucune donnée n'est partagée avec un tiers."
    )
