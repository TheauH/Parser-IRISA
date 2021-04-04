# -*- coding: utf-8 -*-
from enum import Enum, auto
from PyPDF2 import generic
from typing import Dict, List, Set, Tuple, Union

from .page import Première_page
from .champ import Champ
from .transcription import Transcription
from .strop import format_nom, format_courriel, recherche_sans_accents


class typeDonnée(Enum):
    nom = auto()
    affiliation = auto()
    courriel = auto()


class SousLigne:
    """
    Représente une partie de ligne
    donnant une information d’un type donné
    """

    def __init__(
        self, typeD: typeDonnée = typeDonnée.affiliation, coordonnées: Tuple[int] = ()
    ) -> None:
        self.type = typeD
        self.coordonnées = coordonnées  # (ligne, colonne début, colonne fin)

    def contenu(self, bloc_relatif: List[str]) -> str:
        """
        Texte porté par la sous-ligne, en considérant qu’elle est
        définie relativement au bloc `bloc_relatif`
        """
        return bloc_relatif[self.coordonnées[0]][
            self.coordonnées[1] : self.coordonnées[2]
        ]

    def est_face_à(self, sousBloc: "SousBloc") -> bool:
        """
        Indique si la sous-ligne a des colonnes en commun
        avec un sous-bloc donné
        """
        return (
            self.coordonnées[2] > sousBloc.coordonnées[1]
            and sousBloc.coordonnées[3] > self.coordonnées[1]
        )


class SousBloc:
    """
    Représente une colonne à l’intérieur de la section des auteurs,
    correspondant en principe soit à un seul auteur, soit à un ensemble
    d’auteurs partageant les mêmes coordonnées
    """

    def __init__(self, sousLigne: SousLigne, auteurs: Set["Auteur"] = set()) -> None:
        self.sousLignes = [sousLigne]
        self.auteurs = auteurs or set()
        self.coordonnées: Tuple[int] = (
            sousLigne.coordonnées[0],  # ligne début
            sousLigne.coordonnées[1],  # colonne début
            sousLigne.coordonnées[0],  # ligne fin
            sousLigne.coordonnées[2],  # colonne fin
        )

    def ajoute(self, sousLigne: "SousLigne") -> None:
        """
        Ajoute une sous-ligne
        """
        self.sousLignes.append(sousLigne)
        self.coordonnées = (
            min(self.coordonnées[0], sousLigne.coordonnées[0]),
            min(self.coordonnées[1], sousLigne.coordonnées[1]),
            max(self.coordonnées[2], sousLigne.coordonnées[0]),
            max(self.coordonnées[3], sousLigne.coordonnées[2]),
        )


class Auteur:
    """
    Représente un auteur et ses coordonnées
    """

    def __init__(self, nom: str, courriel: str = "", affiliation: str = "") -> None:
        self.nom = nom
        self.courriel = courriel
        self.affiliation = affiliation
        print("nouvel auteur avec le nom", self.nom)

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
            nom="auteurs",
            contenu=[],
            ligne_début=début_bloc,
            ligne_fin=Auteur.fin_bloc(page),
        )

        # La séquence de lignes à explorer
        bloc = page[champ_auteurs.ligne_début : champ_auteurs.ligne_fin]

        # Liste des sous-blocs composant la section
        sousBlocs: List[SousBloc] = []

        """
        Recherche des lignes d’adresses électroniques,
        car il est facile de reconnaître plusieurs courriels à la suite
        pour séparer les blocs.
        """
        les_blocs_sont_délimités_par_les_courriels = False
        for l, ligne in enumerate(bloc):
            courriels_trouvés = [
                SousLigne(
                    typeD=typeDonnée.courriel,
                    coordonnées=(l, ct.span()[0], ct.span()[1]),
                )
                for ct in format_courriel.finditer(ligne)
            ]
            if not sousBlocs and len(courriels_trouvés) >= 2:
                les_blocs_sont_délimités_par_les_courriels = True
            for ct in courriels_trouvés:  # Un sous-bloc par adresse
                courriel_ajouté: bool = False
                for sb in sousBlocs:
                    if ct.est_face_à(sb):
                        sb.sousLignes.append(ct)
                        courriel_ajouté = True
                if not courriel_ajouté:
                    sousBlocs.append(SousBloc(ct))

        """
        Retour au sommet de la section, où l’on recherche
        les noms des auteurs.
        """
        méta_fiable = False
        if métaauteurs:
            métaliste: List[str] = [auteur.strip() for auteur in métaauteurs.split(";")]
            auteurs_trouvés: List[SousLigne] = []
            for auteur in métaliste:
                auteur_trouvé = recherche_sans_accents(auteur, bloc[0])
                if auteur_trouvé:
                    auteurs_trouvés.append(
                        SousLigne(
                            typeDonnée.nom,
                            (0, auteur_trouvé.span()[0], auteur_trouvé.span()[1]),
                        )
                    )
            if auteurs_trouvés:
                méta_fiable: bool = True
        if not méta_fiable:
            auteurs_trouvés = [
                SousLigne(typeDonnée.nom, (0, at.span()[0], at.span()[1]))
                for at in format_nom.finditer(bloc[0])
            ]
        for at in auteurs_trouvés:
            print(at.contenu(bloc))
            objAuteur = Auteur(at.contenu(bloc))
            champ_auteurs.contenu.append(objAuteur)
            at_ajouté = False
            if sousBlocs:
                for sb in sousBlocs:
                    if at.est_face_à(sb):
                        sb.ajoute(at)
                        at_ajouté = True
                        sb.auteurs.add(objAuteur)
            if not at_ajouté:
                sousBlocs.append(SousBloc(at, {objAuteur}))

        # Parcours et classement des lignes et sous-lignes du bloc
        for ligne in bloc:
            pass

        # Attribution des courriels aux auteurs
        for sousBloc in sousBlocs:
            adresses = list(
                filter(lambda sl: sl.type == typeDonnée.courriel, sousBloc.sousLignes)
            )
            for auteur, adresse in zip(sousBloc.auteurs, adresses):
                auteur.courriel = adresse.contenu(bloc)

        # Retrait d’un espace éventuel dû à l’expression régulière
        for auteur in champ_auteurs.contenu:
            auteur.nom = auteur.nom.rstrip()

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