"""Navigation Amazon.fr et collecte Selenium avec pagination et sélection aléatoire."""
import logging
import random
from urllib.parse import quote_plus

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.scraper.driver import creer_driver
from app.scraper.parsing import analyser_cartes
from config import BASE_URL, MAX_PAGES, PAGE_LOAD_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)
CARTE = "div[data-component-type='s-search-result']"


class AmazonScraper:
    def __init__(self, timeout: int = PAGE_LOAD_TIMEOUT_SECONDS):
        self.timeout = timeout

    def scraper(self, categorie: str, limite: int, headless: bool = False):
        driver = creer_driver(headless=headless)
        produits, deja_vus = [], set()
        try:
            driver.set_page_load_timeout(self.timeout)
            # On explore plusieurs pages pour avoir un réservoir de produits et pouvoir en piocher de manière aléatoire
            for page in range(1, MAX_PAGES + 1):
                url = f"{BASE_URL}/s?k={quote_plus(categorie)}&page={page}"
                logger.info("Page %s : %s", page, url)
                driver.get(url)
                try:
                    WebDriverWait(driver, self.timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, CARTE))
                    )
                except TimeoutException:
                    logger.warning("Attente dépassée pour %s sur la page %s. Vérification directe...", CARTE, page)
                
                nouveaux = analyser_cartes(driver, BASE_URL, categorie, deja_vus)
                if not nouveaux:
                    logger.warning("Aucun nouveau produit trouvé sur la page %s.", page)
                    if page == 1:
                        # Si même la première page ne donne rien après tentative
                        break
                produits.extend(nouveaux)
                # Si on a assez de produits pour faire un tirage aléatoire varié
                if len(produits) >= max(limite + 15, 30):
                    break

            if not produits:
                raise RuntimeError(
                    f"Aucun produit détecté (CAPTCHA ou page modifiée ?). Titre de page : {driver.title}"
                )

            # Sélection aléatoire de 15 à 20 produits
            nombre_final = min(limite, len(produits))
            selection_aleatoire = random.sample(produits, nombre_final)
            return selection_aleatoire
        except WebDriverException as exc:
            raise RuntimeError(f"Erreur du navigateur Selenium : {exc}") from exc
        finally:
            driver.quit()
