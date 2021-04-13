from .champ import Champ
from .transcription import Transcription


def find_conclusion(transcri: Transcription):
    """ motif rechercher : """
    string = "Conclusion"
    string1 = "VI. CONCLUSION"
    string2 = "5 Conclusion"
    string3 = "ONCLUSION"
    stringbis = "FUTURE WORK"
    string4 = "Acknowledgement"
    string5 = "Acknowledgment"
    string6 = "Reference"
    string7 = "D ISCUSSION"
    string8 = "Discussion"
    string9 = "R EFERENCES"
    string10 = "7       Follow-Up Work"

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
                or (string1 in transcri[np][nl])
                or (string2 in transcri[np][nl])
                or (string3 in transcri[np][nl])
                or (stringbis in transcri[np][nl])
            ):
                page = np
                ligne = nl

            if (
                (string4 in transcri[np][nl])
                or (string5 in transcri[np][nl])
                or (string6 in transcri[np][nl])
                or (string7 in transcri[np][nl])
                or (string8 in transcri[np][nl])
                or (string9 in transcri[np][nl])
                or (string10 in transcri[np][nl])
            ):
                page1 = np
                ligne1 = nl

        # sort de la boucle après que page et page1 soit trouvé
        if page and page1:
            break

    # si le début n'est pas trouvé, rendre vide
    if page == 0:
        return None

    # si la fin est avant le début, prendre les 3 lignes après le début
    if page > page1:
        page1 = page
        ligne1 = ligne + 3

    # géré la première page s'il n'y a qu'une ou plusieurs page à prendre
    if page < page1:
        result = "\n".join(transcri[page][ligne : len(transcri[page]) - 1])
        ligne = 0
        page += 1
    else:
        return Champ(
            nom="conclusion",
            contenu="\n".join(transcri[page][ligne : ligne1 - 1]),
            page_début=page,
            ligne_début=ligne,
            page_fin=page,
            ligne_fin=ligne1 - 1,
        )

    # boucle pour avoir toute lignes rajouté
    while page < page1:
        result += "\n".join(transcri[page][0 : len(transcri[page]) - 1])
        page += 1
    return Champ(
        nom="conclusion",
        contenu=result + "\n".join(transcri[page][ligne : ligne1 - 1]),
        page_début=page,
        ligne_début=ligne,
        page_fin=page,
        ligne_fin=ligne1 - 1,
    )


"""Test sur un document"""
if __name__ == "__main__":
    fi = r"C:\Users\sosob\Parser-IRISA\Parser-IRISA\test\Corpus_2021\Boudin-Torres-2006.pdf"
    t = r"C:\Users\sosob\Parser-IRISA\Parser-IRISA\test\Corpus_2021\Das_Martins.pdf"
    # references(t)
    print(find_conclusion(t))