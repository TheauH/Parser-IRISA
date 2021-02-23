from .transcription import Transcription


class Article:
    """
    Représente un article scientifique muni de son texte complet
    et de ses différents champs (titre, auteurs, résumé, etc.)
    """

    def __init__(
        self,
        texte: Transcription,
        nom: str = "",
        titre: str = "",
        auteurs: list[str] = [],
        résumé: str = "",
    ):
        """
        Constructeur principal, le seul paramètre obligatoire
        est la transcription de l’article, objet `Transcription`.
        """
        self.texte = texte  # La transcription du fichier d’origine
        self.nom = nom  # Le nom du fichier d’origine
        self.titre = titre
        self.auteurs = auteurs
        self.résumé = résumé

    