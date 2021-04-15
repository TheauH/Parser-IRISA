from sys import argv
from pathlib import Path

# from os import *
from os import scandir, mkdir, path
from shutil import rmtree
from .menu import choixSortiePDF, menu

from .article import Article

# menu=True if(len(argv)==2 and argv[1]==menu) else menu = False
men = False  # argument par défaut
if len(argv) >= 3 and argv[1] == "menu":
    men = True
elif len(argv) >= 3:
    men = False
else:
    print("Usage :", argv[0], "dossier (-t|-x)")
    """TODO Meilleure doc (trouver un module dédié ?)"""
    exit(1)
# menu = False
if men is False:
    if len(argv) < 3:
        print("Usage :", argv[0], "dossier (-t|-x)")
        """TODO Meilleure doc (trouver un module dédié ?)"""
        exit(1)

    if not argv[2] in ("-t", "-x"):
        print("Erreur : format incorrect.\nFormats acceptés : -t (texte) ; -x (xml)")
        exit(1)

    demandeXML = argv[2] == "-x"  # Si l’utilisateur demande une sortie en X.M.L.

    chemin_entrées = Path(argv[1])
    chemin_sorties = chemin_entrées / ("xml" if demandeXML else "txt")

    try:
        dossier_entrées = scandir(
            chemin_entrées
        )  # itérateur sur les fichiers de l’entrée
    except NotADirectoryError:
        print("Erreur :", chemin_entrées, "n’est pas un dossier.")
        exit()

    # Suppression s’il y a lieu, et création du dossier de sortie

    rmtree(chemin_sorties, ignore_errors=True)
    mkdir(chemin_sorties)

    # Traitement de chaque fichier P.D.F.
    for entrée in dossier_entrées:
        if entrée.name.endswith(".pdf") and entrée.is_file:
            art = Article(chemin_entrées / entrée.name)
            éléments_article = [
                art.nom,
                art.titre,
                art.auteurs,
                art.résumé,
                art.introduction,
                art.conclusion,
                art.discussion,
                art.references,
            ]
            if demandeXML:  # Si demande une sortie en X.M.L.
                with open(chemin_sorties / (entrée.name[:-3] + "xml"), "wb") as sortie:
                    for élément in éléments_article:
                        if élément:
                            sortie.write(élément.xml().encode() + b"\n")

            else:  # Si demande une sortie en texte
                with open(chemin_sorties / (entrée.name[:-3] + "txt"), "wb") as sortie:
                    for élément in éléments_article:
                        if élément:
                            sortie.write(élément.txt().encode() + b"\n")

else:  # si menu saisie en argument :
    # print("bonjour")
    """TODO : voir si on précise s'il veut txt ou xml ?"""
    if not argv[2] in ("-t", "-x"):  # on test argument 2 : si demande xml ou txt
        print("Erreur : format incorrect.\nFormats acceptés : -t (texte) ; -x (xml)")
        exit(1)

    demandeXML = argv[2] == "-x"  # Si l’utilisateur demande une sortie en X.M.L.

    chemin_entrées = Path(choixSortiePDF())
    chemin_sorties = chemin_entrées / ("xml" if demandeXML else "txt")

    # Suppression s’il y a lieu, et création du dossier de sortie

    rmtree(chemin_sorties, ignore_errors=True)
    mkdir(chemin_sorties)

    # traitement de chaque pdf :
    pdf = menu()
    print(pdf)

    # itérer sur les pdfs sortie :
    listNom = []
    for f in pdf:
        listNom.append(path.basename(Path(f)))
    print(listNom)

    zipped = zip(pdf, listNom)
    for entrée, nom in zipped:
        art = Article(entrée)
        éléments_article = [
            art.nom,
            art.titre,
            art.auteurs,
            art.résumé,
            art.introduction,
            art.conclusion,
            art.discussion,
            art.references,
        ]
        if demandeXML:  # si on demande une sortie xml
            with open(chemin_sorties / (nom[:-3] + "xml"), "wb") as sortie:
                for élément in éléments_article:
                    if élément:
                        sortie.write(élément.xml().encode() + b"\n")
        else:  # si sortie texte :
            with open(chemin_sorties / (nom[:-3] + "txt"), "wb") as sortie:
                for élément in éléments_article:
                    if élément:
                        sortie.write(élément.txt().encode() + b"\n")
