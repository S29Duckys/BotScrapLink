# BotScrapLink - Documentation Complète

## Description

BotScrapLink est un bot Python avancé qui scrape automatiquement des informations d'anime depuis un site web. Il extrait les URLs des épisodes, détecte les lecteurs vidéo compatibles, valide les liens, et permet de télécharger les contenus en masse.

### Fonctionnalités principales

- Scraping du catalogue complet d'anime
- Extraction des épisodes par saison et langue
- Détection automatique des lecteurs vidéo
- Validation des liens (vérification de la disponibilité)
- Export en JSON
- Téléchargement automatique des épisodes
- Support multilingue (VF, VOSTFR, VO)
- Interface interactive pour saisie personnalisée

---

## Structure du projet

```
BotScrapLink/
├── .env                    # Variables d'environnement (à créer)
├── .exempl.env             # Exemple de configuration
├── .gitignore              # Fichiers ignorés par Git
├── pyproject.toml          # Configuration et dépendances
├── README.md               # Documentation
├── catalogue.json          # Catalogue des anime (1000+)
├── results.json            # Résultats du scraping
├── src/
│   └── bot/
│       ├── __init__.py     # Initialisation du package
│       ├── scraper.py      # Moteur de scraping principal
│       └── catalogue.py    # Scraping du catalogue
└── tests/
    └── __init__.py         # Dossier pour les tests
```

---

## Installation

### Prérequis

- Python >= 3.13
- pip ou Poetry
- yt-dlp pour le téléchargement vidéo

### Étape 1 : Cloner le projet

```bash
git clone <url-du-repo>
cd BotScrapLink
```

### Étape 2 : Configurer les variables d'environnement

```bash
cp .exempl.env .env
```

Modifiez `.env` :

```env
URL_SITE_CATALOGUE=https://anime-sama.tv/catalogue/
```

### Étape 3 : Installer les dépendances

#### Avec Poetry (recommandé)

```bash
poetry install
```

#### Avec pip

```bash
pip install -r requirements.txt
```

---

## Utilisation

### Lancer le scraping automatique

```bash
poetry run python -m src.bot.scraper
```

Processus complet :
1. Scrape toutes les saisons de tous les anime
2. Valide les liens (teste chaque URL)
3. Détecte les lecteurs vidéo
4. Exporte les résultats en JSON
5. Lance le téléchargement

### Scraper seulement le catalogue

```bash
poetry run python -m src.bot.catalogue
```

Cela met à jour `catalogue.json` avec les derniers anime disponibles.

### Interface interactive

Lors du lancement, vous pouvez entrer manuellement les anime à scraper :

```
Anime > attack-on-titan
Anime > demon-slayer
Anime > /
```

Commandes disponibles :
- Entrer un slug d'anime : Scraper cet anime
- `/` : Terminer l'entrée
- `!` : Afficher la liste des anime

---

## Fonctionnalités détaillées

### 1. Scraping du Catalogue

```python
from src.bot.catalogue import scrape_catalogue, export_json

animes = scrape_catalogue()
export_json(animes, "catalogue.json")
```

Résultat : Fichier JSON avec 1000+ anime et leurs slugs

### 2. Scraping des saisons et épisodes

```python
from src.bot.scraper import build_urls_from_catalogue

episodes_urls = build_urls_from_catalogue("catalogue.json")
```

Pour chaque anime, détecte :
- Saisons disponibles (1-100)
- Langues disponibles (VF, VOSTFR, VO)
- Lecteurs vidéo compatibles
- Tous les épisodes et leurs URLs

### 3. Validation des liens

```python
from src.bot.scraper import check_link

is_valid = check_link("https://...episode.mp4")
```

Retourne True si le lien est accessible, False sinon

### 4. Détection des lecteurs

Lecteurs supportés :
- Sibnet
- Vidmoly
- SendVid
- Anime-sama (site)

### 5. Téléchargement automatique

```python
from src.bot.scraper import download_from_json

download_from_json("results.json")
```

Crée une structure de dossiers :

```
downloads/
├── attack-on-titan/
│   ├── season1/
│   │   ├── Episode 1 VF.mp4
│   │   ├── Episode 2 VF.mp4
│   │   └── ...
│   └── season2/
└── demon-slayer/
    ├── season1/
    └── ...
```

---

## Dépendances

| Package | Version | Utilité |
|---------|---------|---------|
| requests | >=2.32.5 | Requêtes HTTP |
| beautifulsoup4 | >=4.12 | Parsing HTML |
| python-dotenv | >=0.9.9 | Variables d'environnement |
| yt-dlp | >=2024 | Téléchargement vidéo |

Voir pyproject.toml pour la configuration complète.

---

## Configuration

### Fichier `.env`

```env
# URL du catalogue à scraper
URL_SITE_CATALOGUE=https://anime-sama.tv/catalogue/

# Optionnel : délai entre les requêtes (en secondes)
REQUEST_DELAY=1

# Optionnel : dossier de téléchargement
DOWNLOAD_FOLDER=downloads
```

### Fichier `pyproject.toml`

```toml
[tool.poetry.scripts]
scraper = "src.bot.scraper:main"
catalogue = "src.bot.catalogue:main"
```

---

## Fichiers de sortie

### `results.json` - Résultats du scraping

```json
{
  "attack-on-titan": {
    "vf": [
      {
        "season": 1,
        "player": "sibnet",
        "episodes": [
          "https://sibnet.ru/...episode1.mp4",
          "https://sibnet.ru/...episode2.mp4"
        ]
      }
    ],
    "vostfr": [],
    "vo": []
  }
}
```

### `catalogue.json` - Catalogue mis à jour

```json
{
  "attack-on-titan": "Shingeki no Kyojin",
  "demon-slayer": "Demon Slayer",
  "100-jours-avant-ta-mort": "100 Jours Avant Ta Mort"
}
```

---

## Exemples d'utilisation

### Scraper un seul anime

```python
from src.bot.scraper import check_seasons, export_json

result = check_seasons("https://anime-sama.tv/catalogue/attack-on-titan")
export_json({"attack-on-titan": result}, "single_anime.json")
```

### Vérifier disponibilité des saisons

```python
from src.bot.scraper import check_seasons

seasons = check_seasons("https://anime-sama.tv/catalogue/demon-slayer")
print(f"VF disponible : {len(seasons.get('vf', []))} saisons")
print(f"VOSTFR disponible : {len(seasons.get('vostfr', []))} saisons")
```

### Télécharger seulement une langue

Modifiez download_from_json() pour filtrer les langues :

```python
for anime, languages in data.items():
    if "vf" in languages:
        # Télécharger uniquement la VF
```

### Détecter le lecteur vidéo

```python
from src.bot.scraper import detect_player

url = "https://sibnet.ru/video/..."
player = detect_player(url)
print(f"Lecteur détecté : {player}")  # Affiche : sibnet
```

---

## Dépannage

| Problème | Solution |
|----------|----------|
| Erreur ModuleNotFoundError | Exécutez poetry install ou pip install -r requirements.txt |
| Timeout sur les requêtes | Vérifiez votre connexion, augmentez le timeout |
| Liens morts au téléchargement | Les liens peuvent expirer ; re-scraper régulièrement |
| Authentification requise | Modifiez les User-Agent dans session.headers |
| Pas d'anime trouvé | Vérifiez l'URL_SITE_CATALOGUE dans le fichier .env |

---

## Processus de scraping détaillé

### Étape 1 : Récupération du catalogue

Le bot scrape la page de catalogue du site pour obtenir tous les slugs d'anime disponibles.

### Étape 2 : Recherche des saisons

Pour chaque anime, le bot teste les URLs : `/saison1/vf/episodes.js`, `/saison2/vf/episodes.js`, etc.

### Étape 3 : Parsing JavaScript

Extrait les URLs des épisodes depuis les fichiers JavaScript en utilisant des expressions régulières.

### Étape 4 : Validation des liens

Teste chaque lien d'épisode pour vérifier qu'il est accessible (HTTP 200).

### Étape 5 : Détection du lecteur

Identifie le lecteur vidéo utilisé (Sibnet, Vidmoly, SendVid, Anime-sama).

### Étape 6 : Export JSON

Sauvegarde les résultats dans results.json avec la structure :
anime > langue > saison > episodes

### Étape 7 : Téléchargement

Utilise yt-dlp pour télécharger les vidéos avec la meilleure qualité disponible.

---
