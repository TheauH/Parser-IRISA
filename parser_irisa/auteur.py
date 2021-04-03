# -*- coding: utf-8 -*-
import re
from PyPDF2 import generic
from typing import List, Union

from .page import Page, Première_page
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

    def xml(self) -> str:
        return (
            "<auteur>"
            + self.nom
            + (self.courriel and " (" + self.courriel + ")")
            + "</auteur>"
            + (
                self.affiliation
                and "<affiliation>" + self.affiliation + "</affiliation>"
            )
        )

    def txt(self) -> str:
        return (
            self.nom
            + (self.courriel and " <" + self.courriel + ">")
            + (self.affiliation and " (" + self.affiliation + ")")
        )

    format_courriel = re.compile(r"[^ \n]+@[^ \n]+")
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

        # if champ_auteurs.ligne_fin - champ_auteurs.ligne_début > 2:
        #     """
        #     Recherche simple de colonnes à séparer pour l’analyse
        #     """
        #     carte_vide: List[bool] = page.largeur() * [True]  # True = trou
        #     for ligne in page[champ_auteurs.ligne_début : champ_auteurs.ligne_fin]:
        #         for c, caractère in enumerate(ligne):
        #             if caractère != " ":
        #                 carte_vide[c] = False

        #     séparations: List[int] = [0]  # Colonnes sur lesquelles couper le bloc
        #     i = 0  # Parcours de la carte du vide
        #     # 1. parcours de la marge de gauche
        #     while i < len(carte_vide) and carte_vide[i]:
        #         i += 1
        #     vide = False
        #     # 2. Parcours de la partie intéressante
        #     while i < len(carte_vide):
        #         if vide and not carte_vide[i]:  # vide → caractère
        #             séparations.append(i)
        #             vide = False
        #         elif carte_vide[i]:  # caractère → vide
        #             vide = True
        #         i += 1

        #     blocs: List[List[str]] = [[] for _ in séparations]
        #     for ligne in page[champ_auteurs.ligne_début : champ_auteurs.ligne_fin]:
        #         for i in range(1, len(séparations)):
        #             blocs[i - 1].append(ligne[séparations[i - 1] : séparations[i]])
        #         blocs[-1].append(ligne[séparations[-1] :])

        # else:
        #     blocs = [page[champ_auteurs.ligne_début : champ_auteurs.ligne_fin]]

        # for bloc in blocs:
        #     for ligne in bloc:
        #         print(ligne)

        """
        Vérification de la fiabilité des métadonnées :
        on devrait trouver au moins l’un des noms donnés
        sur la première ligne du bloc.
        """
        méta_fiable = False
        if métaauteurs:
            métaliste: List[str] = [auteur.strip() for auteur in métaauteurs.split(";")]
            if any([auteur in page[début_bloc] for auteur in métaliste]):
                méta_fiable = True
                champ_auteurs.contenu = [Auteur(nom=n) for n in métaliste]

        if méta_fiable:
            courriels: List[str] = []
            for ligne in page[champ_auteurs.ligne_début : champ_auteurs.ligne_fin]:
                courriels += Auteur.format_courriel.findall(ligne)

            éléments_adresses: List[List[str]] = [
                re.split(r"[^a-z]+", adresse.split("@")[0]) for adresse in courriels
            ]

            for adresse, courriel in zip(éléments_adresses, courriels):
                for auteur in champ_auteurs.contenu:
                    if not auteur.courriel and (
                        any([élément in auteur.nom.lower() for élément in adresse])
                        or any(
                            [
                                élément in courriel
                                for élément in auteur.nom.lower().split()
                            ]
                        )
                    ):
                        auteur.courriel = courriel
                        break

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

    """ Test de tout le corpus
    dossier_entrées = scandir(Path("../../Corpus_2021"))
    for entrée in dossier_entrées:
        if entrée.name.endswith(".pdf") and entrée.is_file:
            fichier = open(entrée, "rb")
            print("auteur : "+auteur(Transcription(fichier)))
    """
