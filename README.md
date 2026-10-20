# MobiliSmart

Prototype d'application pour Mobility+ — prédiction d'affluence et recommandation de trajet accessible.
Réalisé dans le cadre du mémoire de fin d'étude ISCOD (Master 2 Transformation Digitale, Data et IA).

## Fonctionnalités

- **Authentification** à deux rôles : administrateur et usager
- **Accueil** : présentation du projet
- **Prédiction d'affluence** : estime le niveau d'affluence (Faible/Moyenne/Élevée) d'une station selon la ligne, le jour et l'horaire, à partir d'un modèle de classification entraîné sur les données Mobility+
- **Recommandation de trajet accessible** : propose les stations les mieux adaptées selon le profil d'accessibilité de l'usager
- **Administration** (réservé au rôle admin) : statistiques et graphiques de pilotage, paramétrage du modèle, journal d'accès

## Installation

```bash
pip install -r requirements.txt
python utils/build_database.py   # construit data/app.db à partir du fichier Excel source
streamlit run app.py
```

## Comptes de démonstration

| Rôle  | Identifiant | Mot de passe |
|-------|-------------|--------------|
| Admin | `admin`     | `Admin123!`  |
| Usager| `usager`    | `Usager123!` |

## Structure du projet

```
mobilismart_app/
├── .streamlit/config.toml   # thème (couleurs du mémoire)
├── assets/                  # ressources statiques (logo, images)
├── models/                  # modèle entraîné (modele_affluence.pkl)
├── data/                    # base SQLite de l'application (app.db)
├── pages/                   # une page Streamlit par fonctionnalité
├── utils/                   # auth, accès base de données, recommandation
├── tests/                   # tests unitaires (pytest)
├── app.py                   # point d'entrée : connexion + navigation
└── requirements.txt
```

## Tests

```bash
pip install pytest
pytest tests/
```

## Confidentialité (RGPD)

Les données utilisées sont fictives. Les mots de passe sont hachés (SHA-256), jamais stockés en clair.
Le journal d'accès ne conserve que des informations techniques minimales (identifiant, rôle, horodatage).

## Lien avec le mémoire

Ce code accompagne la Partie 2 (Spécifications techniques) et la Partie 4 (Réalisations et preuves)
du mémoire MobiliSmart. Le notebook `MobiliSmart_ML.ipynb` (dans le dossier technique du mémoire)
documente le nettoyage des données, l'analyse exploratoire et l'entraînement du modèle utilisé ici.
