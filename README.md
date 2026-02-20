# BotScrapLink - README

## Description

BotScrapLink est un bot Python qui scrape des informations d'anime à partir d'un site web. Il permet de récupérer les URLs des saisons disponibles et leurs contenus.

## Structure du projet

```
BotScrapLink/
├── .env                 # Variables d'environnement (à créer)
├── .exempl.env          # Exemple de configuration
├── .gitignore           # Fichiers ignorés par Git
├── pyproject.toml       # Configuration du projet et dépendances
├── README.md            # Ce fichier
├── src/
│   └── bot/
│       ├── __init__.py  # Initialisation du package
│       └── scraper.py   # Script principal de scraping
└── tests/
    └── __init__.py      # Dossier pour les tests
```

## Installation

### Prérequis

- Python >= 3.13
- pip ou Poetry

### Étape 1 : Cloner le projet

```bash
git clone <url-du-repo>
cd BotScrapLink
```

### Étape 2 : Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet :

```bash
cp .exempl.env .env
```

Puis modifiez le fichier `.env` avec votre URL cible :

```
URL_SITE=https://anime-sama.tv/catalogue/
```

### Étape 3 : Installer les dépendances

#### Avec Poetry (recommandé)

```bash
poetry install
```

## Utilisation

### Lancer le script

```bash
poetry run scraper
```

Ou directement avec Python :

```bash
python -m bot.scraper
```

### Commandes disponibles

- **Entrer un nom d'anime** : Saisissez le nom pour le scraper
- **`/`** : Arrêter la saisie
- **`!`** : Afficher la liste des animes saisis

## Dépendances

| Package | Version | Utilité |
|---------|---------|---------|
| `dotenv` | >=0.9.9, <0.10.0 | Gestion des variables d'environnement |
| `requests` | >=2.32.5, <3.0.0 | Requêtes HTTP |

## Configuration du projet

Le projet utilise Poetry pour la gestion des dépendances. Consultez [pyproject.toml](pyproject.toml) pour plus de détails.

**Point d'entrée** : `bot.scraper:main`

## Notes

- Le bot scrape les saisons disponibles avec un timeout de 3-5 secondes
- Les requêtes invalides ou expirant sont gérées avec des messages d'erreur