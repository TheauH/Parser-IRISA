#!/usr/bin/env python3

"""
Comparaison entre les résultats attendus du parsage des fichiers du
corpus test, et les résultats effectifs obtenus par le parseur.
L’option -s (souple) permet d’avoir une tolérance de 10 % sur chaque section.
"""

from typing import Sequence, Union
from os import PathLike, scandir
from sys import argv
from pathlib import Path
import xml.etree.ElementTree as ET
from config import strop, article, auteur
from difflib import SequenceMatcher


def précision(
    art: article.Article, ref: Union[str, bytes, PathLike], souple=False
) -> float:
    """
    Donne la précision de l’article `art`, calculée comme suit :
    Précision=Sections correctes trouvées par le système / Sections véritables.
    Les « sections véritables » sont données par le fichier X.M.L.
    à l’adresse `ref`.
    """
    refXML = ET.parse(ref).getroot()  # Nœud article (racine) de la référence
    champs_art = {
        "preamble": art.nom,
        "titre": art.titre,
        "abstract": art.résumé,
        "introduction": art.introduction,
        "results": art.results,
        "discussion": art.discussion,
        "conclusion": art.conclusion,
        "biblio": art.references,
    }

    sections_correctes = sections_attendues = 0
    for élément in refXML:
        # TODO Mieux prendre en compte le cas de la section « auteurs »
        sections_attendues += 1
        if élément.tag == "auteurs":
            continue  # On voit les auteurs ensuite, indépendamment.
        contenu_attendu = strop.sans_blancs(élément.text)
        contenu_obtenu = strop.sans_blancs(str(champs_art[élément.tag].contenu))

        if (not souple and contenu_attendu == contenu_obtenu) or (
            souple
            and SequenceMatcher(None, contenu_attendu, contenu_obtenu).ratio() >= 0.9
        ):
            sections_correctes += 1

    auteurs = refXML.find("auteurs")
    auteurs_attendus = auteurs_corrects = 0
    auteurs_affiliations: dict[str, str] = {}  # Dictionnaire des auteurs attendus

    for élément in auteurs:  # Parcours pour remplir le dictionnaire
        if élément.tag == "auteur":
            auteurs_affiliations[élément.text] = None
        elif élément.tag == "affiliation":
            for identité, affiliation in reversed(auteurs_affiliations.items()):
                # On remonte la liste des auteurs sans affiliations
                if not affiliation:
                    auteurs_affiliations[identité] = strop.sans_blancs(élément.text)
                else:
                    break

    for chaqueAuteur, sonAffiliation in auteurs_affiliations.items():
        identité = chaqueAuteur.rstrip(")").split(" (")  # [nom, courriel]

        if not identité:  # Cas impossible si le parsage à la main est bien fait
            continue

        auteurs_attendus += 1

        auteurMachine: Union[auteur.Auteur, None] = next(
            (a for a in art.auteurs.contenu if a.nom == identité[0]), None
        )  # récupère l’objet Auteur de même nom

        if not auteurMachine:  # Si l’auteur n’a pas été trouvé du tout
            continue

        if len(identité) == 2 and identité[1] != auteurMachine.courriel:
            # S’il y a un courriel non trouvé
            continue

        if sonAffiliation and sonAffiliation != strop.sans_blancs(
            auteurMachine.affiliation
        ):
            # S’il y a une affiliation incorrecte
            continue

        auteurs_corrects += 1

    précision_auteurs = auteurs_corrects / auteurs_attendus
    if (not souple and précision_auteurs == 1) or (souple and précision_auteurs >= 0.9):
        sections_correctes += 1

    return sections_correctes / sections_attendues


chemin_PDF = Path("test/Corpus TEST")
dossier_PDF = scandir(chemin_PDF)
dossier_résultats = Path("test/Corpus TEST/Parsage manuel")

souplesse = False

souplesse = len(argv) >= 2 and argv[1] == "-s"

for entrée_PDF in dossier_PDF:
    if entrée_PDF.name.endswith(".pdf") and entrée_PDF.is_file:
        art = article.Article(chemin_PDF / entrée_PDF.name)
        print(
            entrée_PDF.name,
            précision(
                art,
                dossier_résultats / (entrée_PDF.name[:-3] + "xml"),
                souple=souplesse,
            ),
        )
