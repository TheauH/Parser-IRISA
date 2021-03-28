# -*- coding: utf-8 -*-
from PyPDF2 import generic
from typing import List, Union

from .page import Première_page
from .champ import Champ
from .transcription import Transcription


class Auteur:
    """
    Représente un auteur et ses coordonnées
    """

    def __init__(self, nom: str, courriel: str = "", affiliation: str = "") -> None:
        self.nom = nom
        self.courriel = courriel
        self.affiliation = affiliation

    def __str__(self) -> str:
        # "Antoine Jamelot <jamelot.e1500523@etud.univ-ubs.fr>"
        return self.nom + (self.courriel and " <" + self.courriel + ">")

    @staticmethod
    def trouve_auteurs(
        trans: Transcription,
        métaauteurs: Union[generic.TextStringObject, None] = None,
        fin_titre: int = 2,
    ) -> Champ:
        page: Première_page = trans[0]
        # Saut du titre :
        i = fin_titre
        while page[i] == "":  # Saute jusqu'au début des auteurs
            i += 1
        if i == 0:
            i = 1  # Les auteurs ne sont jamais sur la première ligne.
        début_bloc = i

        """
        Vérification de la fiabilité des métadonnées :
        on devrait trouver au moins l’un des noms donnés
        sur la première ligne du bloc.
        """
        if métaauteurs:
            métaliste: List[str] = [auteur.strip() for auteur in métaauteurs.split(";")]
            if any([auteur in page[début_bloc] for auteur in métaliste]):
                méta_fiable = True
                return Champ(
                    [Auteur(nom=nom) for nom in métaliste],
                    0,
                    début_bloc,
                    0,
                    Auteur.fin_bloc(page),
                )

        """
        Cas où les métadonnées ne sont pas données ou pas fiables.
        """
        result: List[Auteur] = []  # Liste des auteurs

        fin_bloc = i + 1
        if not hasattr(trans[0], "début_corps"):
            result.append(" ".join(page[i].split()))
        else:

            while i < page.début_corps:
                if not page[i]:
                    i += 1
                    continue
                result.append(Auteur(nom=" ".join(page[i].split())))
                i += 1
                fin_bloc = i

        return Champ(result, 0, début_bloc, 0, fin_bloc)

    def fin_bloc(page: Première_page) -> int:
        """
        Numéro de ligne de fin [exclue] du bloc des auteurs.
        La première page donnée doit être normalisée.
        """
        n = page.début_corps
        while not page[n]:
            n -= 1
        return n + 1

    """ Test de tout le corpus
    dossier_entrées = scandir(Path("../../Corpus_2021"))
    for entrée in dossier_entrées:
        if entrée.name.endswith(".pdf") and entrée.is_file:
            fichier = open(entrée, "rb")
            print("auteur : "+auteur(Transcription(fichier)))
    """

    # erreur avec Iria_Juan-Manuel_Gerardo.pdf, jing-cutepaste.pdf et Torres-moreno1998.pdf
