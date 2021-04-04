"""
Variables et fonctions utiles pour les opérations
sur les chaînes de caractères (str operations)
"""


import re

non_ASCII = re.compile(r"[^\x00-\x7F]")
format_courriel = re.compile(r"[^ \n]+@[^ \n]+")
# [̀-ͯ]


def recherche_sans_accents(pattern, string, flags=0):
    """
    Identique à re.search, à ceci près que chaque lettre de `pattern`
    peut correspondre à la même lettre avec
    """
    return re.search(
        "".join(
            (
                "(i|ı[̀-ͯ])"
                if c == "i"
                else " +"
                if c == " "
                else c + "[̀-ͯ]?"
                if c.isalpha()
                else c
                for c in pattern
            )
        ),
        string,
        flags,
    )
