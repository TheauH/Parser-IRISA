# PASFT

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

Bienvenue sur PASFT!

Ce projet a pour but de produires des résumés d'articles scientifiques, au format texte ou xml. L'outil peut-être utilisé en ligne de commande ou avec un menu graphique tkinter. Cet outil a été créer pour le laboratoires [IRISA](http://www.irisa.fr)

## Pour commencer

L'outil est concu pour les environnements GNU Linux.

### Pré-requis

Ce qu'il est requis pour commencer avec votre projet...

- textract https://pypi.org/project/textract/
- PYPDF2 https://pypi.org/project/PyPDF2/
- pdftotext https://pypi.org/project/pdftotext/

### Installation

Les étapes pour installer votre programme....

Dites ce qu'il faut faire...

_exemple_: Executez la commande ``telnet mapscii.me`` pour commencer ensuite [...]


Ensuite vous pouvez montrer ce que vous obtenez au final...

## Démarrage

Pour lancer l'outil, 2 solutions : 

### En ligne de commande 

'''bash
python3 -m parser_irisa "CHEMIN.../NOMDUDOSSIER/" -t|-x
'''

### Menu tkinter 

'''bash
python3 -m parser_irisa menu -t|-x
'''

### Test de précision

Le dossier `scripts_tests` comprend un script `précision.py`, qui compare les articles obtenus par le parseur avec les articles tels que parsés à la main en X.M.L. La commande est de la forme

```bash
python3 scripts_tests/précision.py [-s]
```

où l’option `-s` (souple) permet une tolérance de 10 % sur la validité de chaque section.

## Fabriqué avec

* [Visual Studio Code](https://code.visualstudio.com)
* [Python](https://www.python.org)

## Versions


**Dernière version stable :**
**Dernière version :** 
Liste des versions : [Cliquer pour afficher](https://github.com/your/project-name/tags)
_(pour le lien mettez simplement l'URL de votre projets suivi de ``/tags``)_

## Auteurs
Listez le(s) auteur(s) du projet ici !
* **Théau Huteau** _alias_ [@TheauH](https://github.com/TheauH)
* **Sofiane Ben Massaoud** _alias_ [@HyziOne](https://github.com/HyziOne)
* **Antoine Jamelot** _alias_ [@Ajamelot56](https://github.com/Ajamelot56)
* **Baptiste Colas** _alias_ [@Genoyd](https://github.com/Genoyd)
