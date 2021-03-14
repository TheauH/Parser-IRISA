"""
@author: Théau Huteau
"""

from .transcription import Transcription

def find_references(transcri):
    texte = Transcription(transcri)
    """ motif rechercher : """
    string = "References"
    string2 = "REFERENCES"
    string3 = "Références"
    """declaration variable contenant le résultat """
    buf = ""
    """compteur de page"""
    p=0
    for i in reversed(range(len(texte))):
        p+=1
        j=0 #compteur de ligne
        for ligne in texte[i]:
            j+=1
            if string in ligne or string2 in ligne or string3 in ligne: 
                break
    n=0
    #on se positionne à la page p et après la ligne n et on renvoie 3 lignes :
    for ligne in texte[p-1]:
        if j>0 and n<5:
            buf+="\n"+ligne.strip()
            n+=1
        else:
            j-=1
    buf+="..."
    return buf


"""Test sur un document"""
if __name__ == "__main__":
    fi = "/Users/theauhuteau/Desktop/MyD/Cours/L3/S2/Conduite-Projet/Corpus_2021/texte/Nasr.txt"
    t = "/Users/theauhuteau/Desktop/MyD/Cours/L3/S2/Conduite-Projet/Corpus_2021/Mikolov.pdf"
    #references(t)
    print(find_references(t))
