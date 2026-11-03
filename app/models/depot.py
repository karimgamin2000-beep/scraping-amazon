"""Dépôt SQLite et export CSV des produits."""
import csv
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path
from typing import Iterable

from app.models.produit import Produit

COLONNES = (
    "id",
    "titre",
    "prix",
    "note",
    "nombre_avis",
    "categorie",
    "date_collecte",
    "reference",
    "image",
)
EN_TETES_EXCEL = (
    "ID",
    "Titre du produit",
    "Prix",
    "Note",
    "Nombre d'avis",
    "Catégorie",
    "Date de collecte",
    "Lien Amazon (URL)",
    "Image (URL)",
)


class DepotProduits:
    def __init__(self, chemin: str | Path):
        self.chemin = Path(chemin)
        self.chemin.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.chemin)) as cx, cx:
            cx.execute(
                """
                CREATE TABLE IF NOT EXISTS produits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titre TEXT NOT NULL,
                    prix TEXT,
                    note TEXT,
                    nombre_avis TEXT,
                    reference TEXT UNIQUE,
                    image TEXT,
                    categorie TEXT,
                    date_collecte TEXT NOT NULL
                )
                """
            )

    def enregistrer(self, produits: Iterable[Produit]) -> int:
        """Insère ou met à jour (clé : reference). Retourne le nombre traité."""
        maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        n = 0
        with closing(sqlite3.connect(self.chemin)) as cx, cx:
            for p in produits:
                cx.execute(
                    """
                    INSERT INTO produits (titre, prix, note, nombre_avis, reference, image, categorie, date_collecte)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(reference) DO UPDATE SET
                        titre=excluded.titre, prix=excluded.prix, note=excluded.note,
                        nombre_avis=excluded.nombre_avis, image=excluded.image,
                        categorie=excluded.categorie, date_collecte=excluded.date_collecte
                    """,
                    (p.titre, p.prix, p.note, p.nombre_avis, p.url, p.image_url, p.categorie, maintenant),
                )
                n += 1
        return n

    def lister(self, categorie: str | None = None) -> list[tuple]:
        requete = f"SELECT {', '.join(COLONNES)} FROM produits"
        params: tuple = ()
        if categorie:
            requete += " WHERE categorie = ?"
            params = (categorie,)
        with closing(sqlite3.connect(self.chemin)) as cx, cx:
            return cx.execute(requete + " ORDER BY id ASC", params).fetchall()

    def exporter_excel(self, dossier: str | Path) -> Path:
        """Génère un vrai fichier Excel (.xlsx) avec colonnes ajustées et en-têtes stylisés."""
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment

        dossier = Path(dossier)
        dossier.mkdir(parents=True, exist_ok=True)
        fichier = dossier / f"produits_tech_{datetime.now():%Y%m%d_%H%M%S}.xlsx"

        wb = Workbook()
        ws = wb.active
        ws.title = "Produits Tech"

        # Ligne d'en-tête
        ws.append(list(EN_TETES_EXCEL))
        header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        
        for col_num in range(1, len(EN_TETES_EXCEL) + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Lignes de données
        lignes = self.lister()
        for ligne in lignes:
            ws.append(list(ligne))

        # Ajustement automatique de la largeur des colonnes
        for col in ws.columns:
            longueur_max = max(len(str(cell.value or '')) for cell in col)
            nom_colonne = col[0].column_letter
            ws.column_dimensions[nom_colonne].width = min(max(longueur_max + 3, 12), 60)

        wb.save(fichier)
        return fichier

    def exporter_csv(self, dossier: str | Path) -> Path:
        """Exporte les données dans un CSV optimisé avec séparateur virgule."""
        dossier = Path(dossier)
        dossier.mkdir(parents=True, exist_ok=True)
        fichier = dossier / f"produits_tech_{datetime.now():%Y%m%d_%H%M%S}.csv"
        with open(fichier, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL)
            w.writerow(EN_TETES_EXCEL)
            w.writerows(self.lister())
        return fichier
