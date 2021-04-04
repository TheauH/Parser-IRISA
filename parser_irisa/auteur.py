# -*- coding: utf-8 -*-
import re
from PyPDF2 import generic
from typing import Dict, List, Tuple, Union

from .page import Première_page
from .champ import Champ
from .transcription import Transcription
from .strop import format_courriel, recherche_sans_accents


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

    def xml(self) -> str:
        return (
            "<auteur>"
            + self.nom
            + (self.courriel and " (" + self.courriel + ")")
            + "</auteur>"
            + (
                self.affiliation
                and "\n<affiliation>\n" + self.affiliation + "\n</affiliation>"
            )
        )

    def txt(self) -> str:
        return (
            self.nom
            + (self.courriel and " <" + self.courriel + ">")
            + (self.affiliation and " (" + self.affiliation + ")")
        )

    # format_courriel = re.compile(
    #     r"(?:(?:[^ \n]|, )+|(?:\{.+\}|\(.+\))[ \n]*)[@Q](?:\n *)?(?:[\w\.\-]|\-\n +)+\.[a-z]{,4}"
    # )

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

        champ_auteurs = Champ(
            nom="auteurs", contenu=[], ligne_début=i, ligne_fin=Auteur.fin_bloc(page)
        )

        # La séquence de lignes à explorer
        bloc = page[champ_auteurs.ligne_début : champ_auteurs.ligne_fin]

        # Les lignes et colonnes de début et de fin (exclue) de chaque auteur
        coordonnées: Dict[Auteur, List[int, int, int, int]] = {}

        """
        Vérification de la fiabilité des métadonnées :
        on devrait trouver au moins l’un des noms donnés
        sur la première ligne du bloc.
        """
        méta_fiable = False
        if métaauteurs:
            métaliste: List[str] = [auteur.strip() for auteur in métaauteurs.split(";")]
            if any(
                (
                    recherche_sans_accents(auteur, page[début_bloc])
                    for auteur in métaliste
                )
            ):
                méta_fiable = True
                champ_auteurs.contenu = [Auteur(nom=n) for n in métaliste]

        # Recherche des courriels et des emplacements des auteurs
        if méta_fiable:
            courriels: List[str] = []
            coord_courriels: List[Tuple[int, int, int, int]] = []
            for l, ligne in enumerate(bloc):
                courriels_trouvés = format_courriel.finditer(ligne)
                for ct in courriels_trouvés:
                    courriels.append(ligne[ct.span()[0] : ct.span()[1]])
                    coord_courriels.append((l, ct.span()[0], l + 1, ct.span()[1]))
                for auteur in champ_auteurs.contenu:
                    if not coordonnées.get(auteur):
                        nom_trouvé = recherche_sans_accents(auteur.nom, ligne)
                        if nom_trouvé:  # Si l’on a trouvé le nom
                            coordonnées[auteur] = [
                                l,
                                nom_trouvé.span()[0],
                                l + 1,
                                nom_trouvé.span()[1],
                            ]
                            auteur.nom = nom_trouvé[0]

            # Attribution des adresses aux auteurs
            for courriel, coord_courriel in zip(courriels, coord_courriels):
                for auteur in champ_auteurs.contenu:
                    """
                    Pour attribuer l’adresse à un auteur, il faut
                    que les deux se trouvent au moins sur une colonne commune.
                    """
                    if (
                        not auteur.courriel
                        and coord_courriel[1] < coordonnées[auteur][3]
                        and coord_courriel[3] > coordonnées[auteur][1]
                    ):
                        auteur.courriel = courriel
                        coordonnées[auteur][2] = coord_courriel[2]  # ligne fin
                        coordonnées[auteur][1] = min(  # colonne début
                            coordonnées[auteur][1], coord_courriel[1]
                        )
                        coordonnées[auteur][3] = max(  # colonne fin
                            coordonnées[auteur][3], coord_courriel[3]
                        )
                        break

            # Recherche des coordonnées d’affiliation de chaque auteur
            for auteur in champ_auteurs.contenu:
                bloc_affiliation: List[str] = []
                for ligne in bloc[
                    coordonnées[auteur][0] + 1 : coordonnées[auteur][2] - 1
                ]:
                    bloc_affiliation.append(
                        ligne[coordonnées[auteur][1] : coordonnées[auteur][3]]
                    )
                auteur.affiliation = "\n".join(bloc_affiliation)

        else:  # = if not méta_fiable:
            liste_auteurs: List[Auteur] = []  # Liste des auteurs

            fin_bloc = i + 1
            if not hasattr(trans[0], "début_corps"):
                liste_auteurs.append(" ".join(page[i].split()))
            else:

                while i < page.début_corps:
                    if not page[i]:
                        i += 1
                        continue
                    liste_auteurs.append(Auteur(nom=" ".join(page[i].split())))
                    i += 1
                    fin_bloc = i

            champ_auteurs.ligne_fin = fin_bloc

        return champ_auteurs

    def fin_bloc(page: Première_page) -> int:
        """
        Numéro de ligne de fin [exclue] du bloc des auteurs.
        La première page donnée doit être normalisée.
        """
        n = page.début_corps - 1
        while not page[n]:
            n -= 1
        return n + 1