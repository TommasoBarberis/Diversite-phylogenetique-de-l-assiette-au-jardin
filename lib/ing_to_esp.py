 # -*- coding: utf-8 -*-

from lib import get_ing
import inspect
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def db_to_dicto (path):
    """
    Pour créer un dictionnaire à partir du fichier ayant les noms scientifiques des espèces (filtered_scientific_name_db.txt).
    Les clefs sont les noms vernaculaires et les valeurs les noms scientifiques.
    """
    f = open(path,"r", encoding='utf-8')
    line = f.readline()
    dicto = {}
    while line:
        colonnes = line.split("\t")
        clee = colonnes[1].replace("\n","")
        valeur = colonnes[0]
        dicto[clee] = valeur
        line = f.readline()
    f.close()
    return dicto


def search_in_dict(correspondences, dicto_esp, liste_ing):
    for k in liste_ing:
        if k in correspondences.keys():
            dicto_esp[k.lower()] = correspondences[k]
        elif k.capitalize() in correspondences.keys():
            dicto_esp[k.lower()] = correspondences[k.capitalize()]
        elif k.endswith("s"):
            k = k[0:-1]
            if k in correspondences.keys():
                dicto_esp[k.lower()] = correspondences[k]
    return dicto_esp


def last_try(ing, dico_espece, score_thresh, caller):
    best_match = []
    best_score = score_thresh
    match_cpt = 1
    for key in dico_espece:
        score = similar(ing, dico_espece[key])
        if score > score_thresh:
            best_match.append([dico_espece[key], key, match_cpt])
            match_cpt = match_cpt+1
            if score > score_thresh:
                best_score = score
    if best_score >= 0.8:
        return best_match[-1][1]
    elif best_match != []: 
        if caller == "main.py":
            selected = int(input("please choose the correct specie's number (from 1 to " + str(len(best_match))\
                 + ")" + " for " + str(ing) + " (if nothing is correct type 0): \n" + str(best_match) ) + "\n")
            if selected != 0 and selected < len(best_match): 
                return best_match[selected-1][1]
            else:
                return None
    else:
        return None


def recherche_globale(dicto_ing):
    """
    Permet de trouver la  correspondance entre les noms vernaculaires des ingrédients et leurs espèces.
    En entrée il prend un dictionnaire ou les clefs sont les noms vernaculaires des ingrédients et retourne
    un dictionnaire avec comme clef les ingrédients et comme valeurs les noms scientifiques des espèces.
    """

    correspondences = db_to_dicto("data/filtered_scientific_name_db.txt")
    dicto_esp = {}
    liste_ing = []
    for k in dicto_ing.keys():
        liste_ing.append(k)
    dicto_esp = search_in_dict(correspondences, dicto_esp, liste_ing)    
    for k in dicto_ing.keys():
        if k not in dicto_esp and k[:len(k)-1] not in dicto_esp:
            caller = inspect.stack()[1].filename  # in order to distinguish the caller between main.py and GUI.py
            specie = last_try(k, correspondences, 0.5, caller)
            if specie is None:
                dicto_esp[k] = '/'
    return dicto_esp


if __name__ == "__main__":

    dicto_ing = {'farine': 200.0, 'beurre demi-sel': 100.0, 'eau': 50.0, 'sel': 1.0, 'crème': 250.0, 'carambar©': 320.0,\
         'chocolat': 100.0, 'beurre de cacahuètes': 2.0}


    print(recherche_globale(dicto_ing))
