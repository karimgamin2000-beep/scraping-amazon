"""Point d'entrée : application console de scraping Amazon.fr (produits tech)."""
import argparse
import logging

from app.controllers.scraping_controller import ScrapingController
from app.models.depot import DepotProduits
from app.views.console_view import ConsoleView
from config import DEFAULT_DATABASE


def main():
    parser = argparse.ArgumentParser(description="Scraper Amazon.fr - produits technologiques")
    parser.add_argument("--headless", action="store_true", help="Chrome sans fenêtre")
    parser.add_argument("--database", default=str(DEFAULT_DATABASE), help="Chemin de la base SQLite")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    ScrapingController(ConsoleView(), DepotProduits(args.database), args.headless).run()


if __name__ == "__main__":
    main()
