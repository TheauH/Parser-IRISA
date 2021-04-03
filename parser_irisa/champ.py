from typing import List, Union


class Champ:
    """
    Représente un champ d’article : titre, auteur, résumé...
    """

    def __init__(
        self,
        nom: str,
        contenu: Union[str, list],
        page_début: int = 0,
        ligne_début: int = 0,
        page_fin: int = 0,
        ligne_fin: int = 0,
    ):
        """
        Le contenu du champ (texte ou autre) doit se retrouver dans sa transcription
        dans l’intervalle :

        [ `transcription[page_début][ligne_début]` ; `transcription[page_fin][ligne_fin]` [
        (début inclus, fin exclue, comme de coutume en Python)
        """
        self.nom = nom
        self.contenu = contenu
        self.page_début = page_début
        self.ligne_début = ligne_début
        self.page_fin = page_fin
        self.ligne_fin = ligne_fin

    def __str__(self) -> str:
        return str(self.contenu)

    def encode(self) -> bytes:
        return str(self.contenu).encode()

    def xml(self) -> str:
        balise = self.nom
        contenu = (
            "\n".join([auteur.xml() for auteur in self.contenu])
            if isinstance(self.contenu, list)  # Cas de la liste d’auteurs
            else self.contenu
        )
        return "<" + balise + ">\n" + contenu + "\n</" + balise + ">"

    def txt(self) -> str:
        contenu = (
            "\n".join([auteur.txt() for auteur in self.contenu])
            if isinstance(self.contenu, list)
            else self.contenu
        )
        return self.nom.capitalize() + " :\n    " + contenu
