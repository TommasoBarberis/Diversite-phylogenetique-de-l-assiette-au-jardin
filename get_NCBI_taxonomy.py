from ete3 import NCBITaxa
ncbi = NCBITaxa()

# Si on veut mettre à jour la base de données :
#ncbi.update_taxonomy_database()

# Permet d'obtenir l'ID NCBI de l'espèce
def get_taxid(liste_espece):
    if not isinstance(liste_espece, list):
        liste_espece=list(liste_espece)
    return ncbi.get_name_translator(liste_espece).values()

if __name__=="__main__":
    #Définition des arguments
    liste_espece = ['Homo sapiens', 'primate']
    tests = get_taxid(liste_espece)
    for test in tests:
        print (test)
