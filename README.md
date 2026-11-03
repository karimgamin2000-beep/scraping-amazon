# Scraper Amazon.fr — produits technologiques

Application console (Selenium) : elle collecte des produits technologiques sur Amazon.fr, les stocke dans SQLite (`data/produits_tech.db`, ouvrable avec DB Browser) et les exporte en Excel et CSV (`exports/`).

## Installation
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Prérequis : Python 3.10+, Google Chrome.

## Lancement
```powershell
python main.py            # Chrome visible
python main.py --headless # sans fenêtre
```
Menu de l'application :
1) **Lancer le scraping automatique** (tire 15 à 20 produits technologiques aléatoires et met à jour automatiquement la base `.db`, le tableur Excel `.xlsx` et le `.csv`).
2) **Voir les produits enregistrés** (affiche les produits directement dans le terminal).
3) **Exporter la base en fichier Excel (.xlsx) et CSV** (génère les deux fichiers et quitte).
4) **Ouvrir la base directement dans DB Browser for SQLite** (lance directement DB Browser sur votre base).
5) **Quitter**.

Table `produits` : titre, prix, note, nombre_avis, reference (URL, unique), image, categorie, date_collecte. Une nouvelle collecte met à jour les produits déjà connus.

Amazon peut afficher un CAPTCHA : le scraper ne le contourne pas et signale l'échec.

## Vérifications CI

GitHub Actions exécute Ruff, vérifie la syntaxe Python et lance les tests unitaires hors ligne sur Python 3.10. Ces tests portent sur le dépôt SQLite temporaire ; la CI ne lance pas Chrome et n'effectue aucune requête vers Amazon.
