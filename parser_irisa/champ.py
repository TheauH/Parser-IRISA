class Champ:
    """
    Représente un champ d’article : titre, auteur, résumé...
    """

    def __init__(
        self, contenu, page_début: int, ligne_début: int, page_fin: int, ligne_fin: int
    ):
        """
        Le contenu du champ (texte ou autre) doit se retrouver dans sa transcription
        dans l’intervalle :

        [ `transcription[page_début][ligne_début]` ; `transcription[page_fin][ligne_fin]` [
        (début inclus, fin exclue, comme de coutume en Python)
        """
        self.contenu = contenu
        self.page_début = page_début
        self.ligne_début = ligne_début
        self.page_fin = page_fin
        self.ligne_fin = ligne_fin

    def __str__(self) -> str:
        return str(self.contenu)

    def encode(self) -> bytes:
        return str(self.contenu).encode()