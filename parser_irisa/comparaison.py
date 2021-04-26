from typing import Union
from .article import Article
from os import PathLike
import xml.etree.ElementTree as ET
from .strop import sans_blancs


def précision(art: Article, ref: Union[str, bytes, PathLike], souple=False) -> float:
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
        "auteurs": art.auteurs,
        "abstract": art.résumé,
        "introduction": art.introduction,
        "results": art.results,
        "discussion": art.discussion,
        "conclusion": art.conclusion,
    }
    sections_correctes = sections_attendues = 0
    for élément in refXML.iter():
        # TODO Mieux prendre en compte le cas de la section « auteurs »
        sections_attendues += 1
        contenu = sans_blancs(
            "".join(élément.itertext()) if élément.tag == "auteurs" else élément.text
        )
        if contenu == sans_blancs(champs_art[élément.tag].contenu):
            sections_correctes += 1

    return sections_correctes / sections_attendues