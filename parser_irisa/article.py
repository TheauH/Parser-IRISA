from os import PathLike, path
from typing import Union, List
import PyPDF2

from .page import Première_page
from .champ import Champ
from .transcription import Transcription
from .title import extract_information as trouve_titre
from .auteur import Auteur
from .pars_abstract import pars_Abstract
from .references import find_references
from .conclusion import find_conclusion
from .discussion import find_discussion
from .introduction import find_introduction


class Article:
    """
    Représente un article scientifique muni de son texte complet
    et de ses différents champs (titre, auteurs, résumé, etc.)
    """

    def __init__(
        self,
        source: Union[str, PathLike],
    ):
        """
        Constructeur principal, le seul paramètre obligatoire
        est la transcription de l’article, objet `Transcription`.
        """

        # Récupération des métadonnées
        with open(source, "rb") as fichier:
            pdf = PyPDF2.PdfFileReader(fichier, strict=False)
            métadonnées = pdf.getDocumentInfo()

        self.nom = Champ(
            nom="preamble", contenu=path.basename(source)
        )  # Nom du fichier d’origine
        self.texte = Transcription(source)

        self.texte.normalise()
        première_page: Première_page = self.texte[0]

        # Faire appel aux fonctions adéquates pour déterminer ces attributs.
        self.titre: Champ = trouve_titre(
            self.texte,
            métatitre=métadonnées
            and métadonnées.title,  # fourni seulement si on a les métadonnées
        )
        self.auteurs: Champ = Auteur.trouve_auteurs(
            self.texte,
            métaauteurs=métadonnées and métadonnées.author,
            fin_titre=self.titre.ligne_fin,
        )

        self.résumé = pars_Abstract(self.texte)
        self.references = find_references(self.texte)
        self.conclusion = find_conclusion(self.texte)
        self.discussion = find_discussion(self.texte)
        self.introduction = find_introduction(self.texte)
