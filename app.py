"""
MobiliSmart — point d'entrée de l'application Streamlit.

Gère l'authentification (comptes admin / user) et construit la navigation
en fonction du rôle connecté. Les pages elles-mêmes vivent dans pages/.
"""

import streamlit as st

from utils.auth import seed_default_accounts, verify_login
from utils.database import log_access

st.set_page_config(page_title="MobiliSmart", page_icon="🚍", layout="wide")

seed_default_accounts()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


def ecran_connexion():
    st.title("🚍 MobiliSmart")
    st.caption("Connexion")

    with st.form("formulaire_connexion"):
        username = st.text_input("Identifiant")
        password = st.text_input("Mot de passe", type="password")
        valider = st.form_submit_button("Se connecter", type="primary")

    if valider:
        role = verify_login(username, password)
        if role:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
            log_access(username, role, "connexion")
            st.rerun()
        else:
            st.error("Identifiant ou mot de passe incorrect.")

    with st.expander("Comptes de démonstration"):
        st.markdown(
            "- **Administrateur** — identifiant `admin`, mot de passe `Admin123!`\n"
            "- **Usager** — identifiant `usager`, mot de passe `Usager123!`"
        )


def deconnexion():
    log_access(st.session_state.get("username", "?"), st.session_state.get("role", "?"), "deconnexion")
    for cle in ("authenticated", "username", "role"):
        st.session_state.pop(cle, None)
    st.rerun()


if not st.session_state.authenticated:
    ecran_connexion()
    st.stop()

# ---------------------------------------------------------------- Navigation
pages_communes = [
    st.Page("pages/accueil.py", title="Accueil", icon="🏠"),
    st.Page("pages/prediction.py", title="Prédiction d'affluence", icon="📈"),
    st.Page("pages/recommandation.py", title="Recommandation de trajet", icon="♿"),
]
pages_admin = [
    st.Page("pages/administration.py", title="Administration", icon="⚙️"),
]

if st.session_state.role == "admin":
    navigation = st.navigation(pages_communes + pages_admin)
else:
    navigation = st.navigation(pages_communes)

with st.sidebar:
    st.write(f"Connecté : **{st.session_state.username}** ({st.session_state.role})")
    if st.button("Se déconnecter"):
        deconnexion()

navigation.run()
