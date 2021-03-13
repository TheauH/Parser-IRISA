from os import PathLike, path
from typing import Union, List

from .transcription import Transcription
from .title import extract_information as trouve_titre
from .auteur import auteur as trouve_auteurs
from .pars_abstract import pars_Abstract
from .page import Première_page


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
        self.nom = path.basename(source)  # Nom du fichier d’origine
        self.texte = Transcription(source)
        début_corps=self.texte[0].trouve_début_corps()

        # Faire appel aux fonctions adéquates pour déterminer ces attributs.
        self.titre = trouve_titre(source, self.texte)
        self.auteurs: List[str] = [trouve_auteurs(self.texte, titre=self.titre, début_corps=début_corps)]

        self.texte.normalise()
        self.résumé = pars_Abstract(self.texte)
