import os
import unittest
from pathlib import Path

from app.models.depot import DepotProduits
from app.models.produit import Produit


class DepotProduitsTests(unittest.TestCase):
    def test_enregistrer_et_mettre_a_jour_un_produit(self):
        chemin_db = Path(__file__).with_name(f".test_depot_{os.getpid()}.sqlite3")
        try:
            depot = DepotProduits(chemin_db)
            produit = Produit(
                titre="Clavier",
                prix="39,99 €",
                url="https://www.amazon.fr/dp/ABC123",
                categorie="informatique",
            )

            self.assertEqual(depot.enregistrer([produit]), 1)
            self.assertEqual(depot.lister("informatique")[0][1], "Clavier")
            self.assertEqual(depot.lister("audio"), [])

            produit.titre = "Clavier mécanique"
            self.assertEqual(depot.enregistrer([produit]), 1)
            produits = depot.lister()
            self.assertEqual(len(produits), 1)
            self.assertEqual(produits[0][1], "Clavier mécanique")
        finally:
            chemin_db.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
