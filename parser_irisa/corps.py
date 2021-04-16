from .champ import Champ
from .transcription import Transcription


def find_corps(transcri: Transcription, champ_debut : Champ, champ_fin : Champ):
    if not(champ_debut): #Cas normalement impossible où champ_debut est vide, mais juste pour être sûr
        return None

    page_debut=champ_debut.page_fin
    ligne_debut=champ_debut.ligne_fin+1

    if champ_fin: #géré le cas ou champ_fin est vide
        page_fin=champ_fin.page_début
        ligne_fin=champ_fin.ligne_début-1
    else:
        page_fin=len(transcri)-1
        ligne_fin=len(page_fin)-1
    
    #Vérifier que l'on est sûr un ligne viable pour le début et la fin
    if ligne_fin<0:
        page_fin-=1
        ligne_fin=len(transcri[page_fin])-1
    
    if ligne_debut==len(transcri[page_debut]):
        page_debut+=1
        ligne_debut=0

    #Vérifier que les information sur les pages et lignes ne soit pas contradictoire
    if page_debut>page_fin:
        return None
    elif page_debut==page_fin:
        if ligne_debut>ligne_fin:
            return None
        else:#Cas ou on a qu'une seul page
            return Champ(
                nom="corps",
                contenu="\n".join(transcri[page_debut][ligne_debut : ligne_fin]),
                page_début=page_debut,
                ligne_début=ligne_debut,
                page_fin=page_fin,
                ligne_fin=ligne_fin,
            )
    else:#Cas avec plusieurs pages
        result=transcri[page_debut][ligne_debut : len(transcri[page_debut])-1]
        i=page_debut+1
        while i<page_fin:
            result+=transcri[i][0:len(transcri[i])-1]
            i+=1
        return Champ(
            nom="corps",
            contenu="\n".join(result+transcri[i][0:ligne_fin]),
            page_début=page_debut,
            ligne_début=ligne_debut,
            page_fin=page_fin,
            ligne_fin=ligne_fin,
        )



