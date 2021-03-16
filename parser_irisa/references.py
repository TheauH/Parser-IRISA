"""
@author: Théau Huteau
"""

from .transcription import Transcription


def find_references(transcri: Transcription):
    """ motif rechercher : """
    string = "References"
    string2 = "REFERENCES"
    string3 = "Références"
    """declaration variable contenant le résultat """
    buf = ""
    """compteur de page"""
    # Page et numéro de la ligne qui nous intéressent
    ligne = 0
    page = 0
    for np in range(len(transcri) - 1, -1, -1):
        for nl in range(len(transcri[np])):
            if (
                (string in transcri[np][nl])
                or (string2 in transcri[np][nl])
                or (string3 in transcri[np][nl])
            ):
                page = np
                ligne = nl
                break
        if page and ligne:
            break
    # n = 0
    # on se positionne à la page p et après la ligne n et on renvoie 3 lignes :
    # for ligne in transcri[-p]:
    #     if j > 0 and n < 5:
    #         buf += "\n" + ligne.strip()
    #         n += 1
    #     else:
    #         j -= 1
    # buf += "..."
    return "\n".join(transcri[page][ligne + 1 : ligne + 4]) + "…"


"""Test sur un document"""
if __name__ == "__main__":
    fi = "/Users/theauhuteau/Desktop/MyD/Cours/L3/S2/Conduite-Projet/Corpus_2021/texte/Nasr.txt"
    t = "/Users/theauhuteau/Desktop/MyD/Cours/L3/S2/Conduite-Projet/Corpus_2021/Mikolov.pdf"
    # references(t)
    print(find_references(t))
