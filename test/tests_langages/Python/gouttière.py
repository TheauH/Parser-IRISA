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

    def get_abscisse(self):
        return self.abscisse

    def set_abscisse(self, n: int):
        self.abscisse = n

    def get_début(self):
        return self.début

    def set_début(self, n: int):
        self.début = n

    def get_fin(self):
        return self.fin

    def set_fin(self, n: int):
        self.fin = n