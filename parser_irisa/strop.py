"""
Variables et fonctions utiles pour les opérations
sur les chaînes de caractères (str operations)
"""


import re

non_ASCII = re.compile(r"[^\x00-\x7F]")
format_nom = re.compile(r"\b(?:[A-Z])(?:(?:\.|[A-Za-zı-ͯ\.]+)[\-’' ]?)+")
format_sousLigne = re.compile(r"(?:[^ ]+ ?)+")
format_courriel = re.compile(r"[^ ]+@[^ ]+")
blancs = re.compile(r"[ \n\r]")


def recherche_sans_accents(pattern, string, flags=0):
    """
    Identique à re.search, à ceci près que chaque lettre de `pattern`
    peut correspondre à la même lettre avec
    """
    return re.search(
        "".join(
            (
                "(i|ı[̀-ͯ])"
                if c == "i" # i ou ı avec diacritique
                else " +"
                if c == " " # espaces en nombre indéterminé
                else c + "[̀-ͯ]?"
                if c.isalpha() # lettre avec ou sans diacritique
                else c
                for c in pattern
            )
        ),
        string,
        flags,
    )


def sans_blancs(chaîne: str) -> str:
    """
    Renvoie la chaîne donnée sans caractère blancs.
    """
    return blancs.sub("", chaîne)