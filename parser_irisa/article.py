from os import PathLike, path
from typing import Union, List

from .transcription import Transcription


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

        # Faire appel aux fonctions adéquates pour déterminer ces attributs.
        self.titre: str
        self.auteurs: List[str]

        # self.texte.normalise() ?
        self.résumé: str
