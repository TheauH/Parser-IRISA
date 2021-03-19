from .transcription import Transcription


def find_discussion(transcri: Transcription):
    """ motif rechercher : """
    string = "Discussion"
    
    """declaration variable contenant le résultat """
    
    """compteur de page"""
    # Page et numéro de la ligne qui nous intéressent
    ligne = 0
    page = 0
    for np in range(len(transcri) - 1, -1, -1):
        for nl in range(len(transcri[np])):
            if (
                (string in transcri[np][nl])
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
    return "\n".join(transcri[page][ligne : ligne + 3]) + "…"


"""Test sur un document"""
if __name__ == "__main__":
    fi = r"C:\Users\sosob\Parser-IRISA\Parser-IRISA\test\Corpus_2021\Boudin-Torres-2006.pdf"
    t = r"C:\Users\sosob\Parser-IRISA\Parser-IRISA\test\Corpus_2021\Das_Martins.pdf"
    # references(t)
    print(find_discussion(t))
