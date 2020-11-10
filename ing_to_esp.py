 # -*- coding: utf-8 -*-

def db_to_dicto (path):
    """
    Pour creer un dictionnaire a partir du fichier ayant les noms scientifiques des especes de M. De Vienne.
    Les clefs sont les noms verniculaires et les valeurs les noms scientifiques.
    """
    f=open(path,"r", encoding='utf-8')
    line=f.readline()
    dicto={}
    while line:
        colonnes=line.split("\t")
        clee= colonnes[1].replace("\n","")
        valeur= colonnes[0]
        dicto[clee]=valeur
        line=f.readline()
    f.close()
    return dicto

def condition (dicto1, dicto2, k):
    k2=k.capitalize()
    if k in dicto1.keys(): 
        dicto2[k.lower()]=dicto1[k]
    elif k2 in dicto1.keys():
        dicto2[k2.lower()]=dicto1[k2]
    return dicto2

def search_in_dict (dicto1, dicto2, liste):
    for k in liste:
        cond=condition(dicto1, dicto2, k)
    return dicto2

def with_endswith (dicto1, dicto2, liste):
    for k in liste:
        if k.endswith("s"):
            a=k[0:-1]
            cond=condition(dicto1, dicto2, a)
    return dicto2

#pas necessair ?
def by_fields (dicto1, dicto2, liste):
    for k in liste:
        if " " in k:
            champs=k.split()
            for i in champs:
                cond=condition(dicto1, dicto2, i)
                if i.endswith("s"):
                    a=i[0:-1]
                    cond=condition(dicto1, dicto2, a)
    return dicto2

def recherche_globale (dicto_ing):
    correspondences=db_to_dicto("scientific_name_db.txt")
    dicto_esp={}
    liste_ing=[]
    for k in dicto_ing.keys():
        liste_ing.append(k)
    etape1=search_in_dict(correspondences, dicto_esp, liste_ing)    
    dicto_final=with_endswith(correspondences,etape1, liste_ing)
    # etape2=with_endswith(correspondences,etape1, liste_ing)
    # dicto_final=by_fields(correspondences, etape2, liste_ing)
    return dicto_final


#################MAIN#########################
if __name__ == "__main__":

    dicto_ing = {'farine': 200.0, 'beurre demi-sel': 100.0, 'eau': 50.0, 'sel': 1.0, 'crème': 250.0, 'carambar©': 320.0, 'chocolat': 100.0, 'beurre de cacahuètes': 2.0}

    #print(liste_ing)

    print(recherche_globale())
