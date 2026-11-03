"""Configuration du scraper Amazon (produits technologiques)."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
BASE_URL = "https://www.amazon.fr"
DEFAULT_SEARCH_TERM = "technologie"
MIN_RANDOM_PRODUCTS = 15
MAX_RANDOM_PRODUCTS = 20
MAX_PAGES = 5
DEFAULT_DATABASE = PROJECT_ROOT / "data" / "produits_tech.db"
EXPORT_DIR = PROJECT_ROOT / "exports"
PAGE_LOAD_TIMEOUT_SECONDS = 30

