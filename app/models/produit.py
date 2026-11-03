"""Modèle représentant un produit technologique trouvé sur Amazon."""
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Produit:
    titre: str
    prix: Optional[str] = None
    note: Optional[str] = None
    nombre_avis: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    categorie: Optional[str] = None

    def to_dict(self):
        return asdict(self)
