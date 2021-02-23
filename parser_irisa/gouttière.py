class Gouttière:
    """
    Représente une ligne verticale sur une page, représentée par
    son abscisse, son début (indice de sa première ligne)
    et sa fin (indice de sa dernière ligne)
    """

    def __init__(self, abscisse: int, première_ligne: int, dernière_ligne: int):
        self.abscisse = abscisse
        self.début = première_ligne
        self.fin = dernière_ligne