def db_to_dicto (path):
    """
    Pour creer un dictionnaire a partir du fichier ayant les noms scientifiques des especes de M. De Vienne.
    Les clefs sont les noms verniculaires et les valeurs les noms scientifiques.
    """
    f=open(path,"r")
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
        dicto2[k]=dicto1[k]
    elif k2 in dicto1.keys():
        dicto2[k2]=dicto1[k2]
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

#################MAIN#########################
correspondences=db_to_dicto("/home/tommaso/Semestre_1/Projet_S1/div-phylo-alim/scientific_name_db.txt")

dicto_ing = {'pulpe de tomates': 400, 'penne': 400, 'parmesan râpé': 75, "c. à s. d'huile d'olive": 3, "gousse d'ail": 1, 'Gros sel': 1, 'c. à c. de poudre de piment': 0.5, 'Sel ou sel fin': 1, 'Basilic pour servir (facultatif)': 1}
liste_ing=[]
for k in dicto_ing.keys():
    liste_ing.append(k)

print(liste_ing)
dicto_esp={}

etape1=search_in_dict(correspondences, dicto_esp, liste_ing)
etape2=with_endswith(correspondences,etape1, liste_ing)
etape3=by_fields(correspondences, etape2, liste_ing)

print(etape3)