from .champ import Champ
from .transcription import Transcription


def find_introduction(transcri: Transcription):
    """ motif rechercher : """
    stringp1_1 = "ntroduction"
    stringp1_2 = "NTRODUCTION"

    """declaration variable contenant le résultat """

    """compteur de page"""
    # Page et numéro de la ligne qui nous intéressent
    ligne = -1
    page = -1
    ligne_fin=-1
    page_fin=-1
    for np in range(len(transcri)):
        for nl in range(len(transcri[np])):
            if (
                (stringp1_1 in transcri[np][nl])
                or (stringp1_2 in transcri[np][nl])
            ):
                page = np
                ligne = nl
            if page!=-1:
                break
        # sort de la boucle après que page est trouvé
        if page!=-1:
            break
    
    if "1. " in transcri[page][ligne]:
        stringp2_1= "2. "
    elif " I. " in transcri[page][ligne]:
        stringp2_1= " II. "
    elif "1  " in transcri[page][ligne]:
        stringp2_1= "2  "
    else:
        stringp2_1= "2"

    for np in range(page, len(transcri)):
        for nl in range(len(transcri[np])):
            if stringp2_1 in transcri[np][nl]:
                page_fin = np
                ligne_fin = nl
            if page_fin!=-1:
                break
        # sort de la boucle après que page de fin est trouvé
        if page_fin!=-1:
            break

    # si la fin est avant le début, prendre les 3 lignes après le début
    if page > page_fin:
        page_fin = page
        ligne_fin = ligne

    # géré la première page s'il n'y a qu'une ou plusieurs page à prendre
    if page < page_fin:
        result = "\n".join(transcri[page][ligne : len(transcri[page]) - 1])
        ligne = 0
        page += 1
    else:
        return Champ(
            nom="introduction",
            contenu="\n".join(transcri[page][ligne : ligne_fin - 1]),
            page_début=page,
            ligne_début=ligne,
            page_fin=page,
            ligne_fin=ligne_fin - 1,
        )

    # boucle pour avoir toute lignes rajouté
    while page < page_fin:
        result += "\n".join(transcri[page][0 : len(transcri[page]) - 1])
        page += 1
    return Champ(
        nom="introduction",
        contenu=result + "\n".join(transcri[page][ligne : ligne_fin - 1]),
        page_début=page,
        ligne_début=ligne,
        page_fin=page,
        ligne_fin=ligne_fin - 1,
    )