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
    page = None
    ligne = 0
    for p in reversed(transcri):
        for nl, l in enumerate(p):
            if string in l or string2 in l or string3 in l:
                page = p
                ligne = nl
                # Champ trouvé
                return "\n".join(page[0:][ligne + 1 : ligne + 100]) 

    # Champ non trouvé
    return "—"


"""Test sur un document"""
if __name__ == "__main__":
    fi = "/Users/theauhuteau/Desktop/MyD/Cours/L3/S2/Conduite-Projet/Corpus_2021/texte/Nasr.txt"
    t = "/Users/theauhuteau/Desktop/MyD/Cours/L3/S2/Conduite-Projet/Corpus_2021/Mikolov.pdf"
    # references(t)
    print(find_references(t))
