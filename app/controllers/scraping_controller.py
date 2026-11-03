"""Contrôleur : relie vue, scraper et dépôt."""
import random
from app.models.depot import DepotProduits
from app.scraper.amazon_scraper import AmazonScraper
from config import DEFAULT_SEARCH_TERM, EXPORT_DIR, MAX_RANDOM_PRODUCTS, MIN_RANDOM_PRODUCTS


class ScrapingController:
    def __init__(self, vue, depot: DepotProduits, headless: bool = False):
        self.vue, self.depot, self.headless = vue, depot, headless
        self.scraper = AmazonScraper()

    def scraping_automatique(self):
        # Nombre aléatoire entre 15 et 20 produits
        nombre_cible = random.randint(MIN_RANDOM_PRODUCTS, MAX_RANDOM_PRODUCTS)
        self.vue.message(f"Collecte automatique en cours sur le thème '{DEFAULT_SEARCH_TERM}' ({nombre_cible} produits ciblés aléatoirement)...")
        try:
            produits = self.scraper.scraper(DEFAULT_SEARCH_TERM, nombre_cible, self.headless)
        except Exception as exc:
            self.vue.message(f"Échec du scraping : {exc}")
            return
        
        # 1. Enregistrement / mise à jour automatique dans la base SQLite (.db)
        n = self.depot.enregistrer(produits)
        self.vue.message(f"[1/3] Base de données SQLite mise à jour : {n} produit(s) enregistrés dans {self.depot.chemin}")
        
        # 2. Export automatique simultané au format Excel (.xlsx natif)
        fichier_xlsx = self.depot.exporter_excel(EXPORT_DIR)
        self.vue.message(f"[2/3] Fichier Excel généré (.xlsx) : {fichier_xlsx}")

        # 3. Export automatique simultané au format CSV
        fichier_csv = self.depot.exporter_csv(EXPORT_DIR)
        self.vue.message(f"[3/3] Fichier CSV généré (.csv) : {fichier_csv}")
        self.vue.message("Tous les exports (.db, .xlsx et .csv) sont terminés avec succès.")
        self.vue.message("Opération terminée. Fermeture de l'application.")
        return True  # Quitter directement après le scraping et les exports

    def voir(self):
        self.vue.afficher_produits(self.depot.lister())

    def exporter(self):
        fichier_xlsx = self.depot.exporter_excel(EXPORT_DIR)
        fichier_csv = self.depot.exporter_csv(EXPORT_DIR)
        self.vue.message(f"Export Excel (.xlsx) réussi : {fichier_xlsx}")
        self.vue.message(f"Export CSV (.csv) réussi : {fichier_csv}")
        self.vue.message("Exports terminés. Fermeture de l'application.")
        return True  # Signal pour quitter l'application

    def ouvrir_db_browser(self):
        import subprocess
        from pathlib import Path
        chemin_db = Path(self.depot.chemin).resolve()
        exe_browser = Path(r"C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe")
        if not exe_browser.exists():
            self.vue.message(f"DB Browser introuvable à l'emplacement standard ({exe_browser}).")
            self.vue.message(f"Veuillez ouvrir manuellement le fichier : {chemin_db}")
            return
        try:
            subprocess.Popen([str(exe_browser), str(chemin_db)])
            self.vue.message(f"Ouverture de DB Browser for SQLite avec la base : {chemin_db}")
        except Exception as exc:
            self.vue.message(f"Erreur lors du lancement de DB Browser : {exc}")

    def run(self):
        while True:
            try:
                choix = self.vue.menu()
            except (EOFError, KeyboardInterrupt):
                self.vue.message("\nFermeture.")
                break
            if choix == "1":
                quitter = self.scraping_automatique()
                if quitter:
                    break
            elif choix == "2":
                self.voir()
            elif choix == "3":
                quitter = self.exporter()
                if quitter:
                    break
            elif choix == "4":
                self.ouvrir_db_browser()
            elif choix == "5":
                self.vue.message("Au revoir.")
                break
            else:
                self.vue.message("Choix invalide. Veuillez saisir 1, 2, 3, 4 ou 5.")
