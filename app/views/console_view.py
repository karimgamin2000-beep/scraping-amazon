"""Interface console : menu et affichage."""


class ConsoleView:
    MENU = (
        "\n=== Scraper Amazon.fr - Produits Technologiques ===\n"
        "1) Lancer le scraping automatique (15 à 20 produits aléatoires)\n"
        "2) Voir les produits enregistrés dans la base SQLite\n"
        "3) Exporter la base en fichier Excel (.xlsx) et CSV\n"
        "4) Ouvrir la base directement dans DB Browser for SQLite\n"
        "5) Quitter\n"
    )

    def menu(self) -> str:
        print(self.MENU)
        return input("Votre choix : ").strip()

    def message(self, texte: str):
        print(texte)

    def afficher_produits(self, lignes):
        """lignes : tuples (id, titre, prix, note, nombre_avis, categorie, date_collecte, reference, image)."""
        if not lignes:
            print("Aucun produit enregistré pour le moment.")
            return
        for id_, titre, prix, note, avis, cat, date, ref, _img in lignes:
            print(f"[{id_}] {titre[:80]}")
            print(f"     Prix: {prix or '-'} | Note: {note or '-'} | Avis: {avis or '-'} | Catégorie: {cat} | Date: {date}")
            print(f"     Lien: {ref}")
        print(f"\nTotal : {len(lignes)} produit(s) dans la base.")

