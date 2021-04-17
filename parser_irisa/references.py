"""
@author: Théau Huteau
"""

from .transcription import Transcription
from .champ import Champ


def find_references(transcri: Transcription):
    """ motif rechercher : """
    string = "References"
    string2 = "REFERENCES"
    string3 = "Références"
    string4 = "R EFERENCES"
    stringend = "ù"
    """declaration variable contenant le résultat """
    """compteur de page"""
    # Page et numéro de la ligne qui nous intéressent
    ligne = 0
    page = 0
    ligne1 = 0
    page1 = 0
    i = 0
    k = 0
    for np in range(len(transcri) - 1, -1, -1):
        for nl in range(len(transcri[np]) - 1, -1, -1):
            if (
                (string in transcri[np][nl])
                or (string2 in transcri[np][nl])
                or (string3 in transcri[np][nl])
                or (string4 in transcri[np][nl])
                ):
                page = np
                ligne = nl
            if stringend in transcri[np][nl]:
                page1 = np
                ligne1 = nl

        # sort de la boucle après que page et page1 soit trouvé
        if page and page1:
            break

    # si le début n'est pas trouvé, rendre vide
    if page == 0:
        return None

    if page > page1:
        result = "\n".join(transcri[page][ligne : len(transcri[page]) - 1])
        ligne = 0
        page += 1
    else:
        return Champ(
            nom="Reference",
            contenu="\n".join(transcri[page][ligne : ligne1 - 1]),
            page_début=page,
            ligne_début=ligne,
            page_fin=page,
            ligne_fin=ligne1 - 1,
        )

    while page < page1:
        result += "\n".join(transcri[page][0 : len(transcri[page]) - 1])
        page += 1
    return Champ(
        nom="Reference : ",
        contenu=result + "\n".join(transcri[page][ligne : ligne1 - 1]),
        page_début=page,
        ligne_début=ligne,
        page_fin=page,
        ligne_fin=ligne1 - 1,
    )



"""Test sur un document"""
if __name__ == "__main__":
    fi = "/Users/theauhuteau/Desktop/MyD/Cours/L3/S2/Conduite-Projet/Corpus_2021/texte/Nasr.txt"
    t = "/Users/theauhuteau/Desktop/MyD/Cours/L3/S2/Conduite-Projet/Corpus_2021/Mikolov.pdf"
    # references(t)
    print(find_references(t))
