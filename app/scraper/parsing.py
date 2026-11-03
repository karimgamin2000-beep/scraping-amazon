"""Extraction des champs produit depuis les résultats Amazon."""
import re
from urllib.parse import urljoin

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from app.models.produit import Produit


def _valeur(element, selecteurs):
    for sel in selecteurs:
        try:
            champ = element.find_element(By.CSS_SELECTOR, sel)
        except NoSuchElementException:
            continue
        for attr in ("aria-label", "title", "textContent"):
            v = champ.get_attribute(attr)
            if v and v.strip():
                return " ".join(v.split())
    return None


def _nombre_avis(carte):
    for sel in ("a[href*='customerReviews'] span", "a.s-underline-text span", "span.s-underline-text"):
        for champ in carte.find_elements(By.CSS_SELECTOR, sel):
            v = " ".join((champ.get_attribute("textContent") or "").split())
            if (v and any(c.isdigit() for c in v) and "publicit" not in v.lower()
                    and "€" not in v and re.fullmatch(r"\(?[\d\s.,]+\s*[kKmM]?\)?", v)):
                return v
    return None


def analyser_cartes(driver, base_url: str, categorie: str, deja_vus: set) -> list[Produit]:
    """Retourne les produits de la page courante, hors ASIN déjà vus."""
    produits = []
    for carte in driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']"):
        asin = carte.get_attribute("data-asin")
        if not asin or asin in deja_vus:
            continue
        titre = _valeur(carte, ["h2 a span", "h2 span", "h2"])
        if not titre:
            continue
        deja_vus.add(asin)
        try:
            img = carte.find_element(By.CSS_SELECTOR, "img.s-image")
            image = img.get_attribute("src") or img.get_attribute("data-src")
        except NoSuchElementException:
            image = None
        produits.append(Produit(
            titre=titre,
            prix=_valeur(carte, [".a-price .a-offscreen", "span.a-price"]),
            note=_valeur(carte, [".a-icon-star-small .a-icon-alt", ".a-icon-alt"]),
            nombre_avis=_nombre_avis(carte),
            url=urljoin(base_url, f"/dp/{asin}"),
            image_url=image,
            categorie=categorie,
        ))
    return produits
