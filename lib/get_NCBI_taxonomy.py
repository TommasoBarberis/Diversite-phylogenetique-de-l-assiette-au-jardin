#  -*- coding: utf-8 -*-

from ete3 import NCBITaxa # , Tree
# import ing_to_esp
import itertools
ncbi = NCBITaxa()

# Si on veut mettre à jour la base de données :
# ncbi.update_taxonomy_database()


# Permet d'obtenir l'ID NCBI de l'espèce
def get_taxid(liste_espece):
    liste_espece = liste_espece.values()
    if not isinstance(liste_espece, list):
        liste_espece=list(liste_espece)
    # Obtention des valeurs du dictionnaire
    Liste = [(ncbi.get_name_translator(liste_espece).values())]
    # Obtention d'une liste des valeurs du dictionnaire
    liste_nettoyée = list(itertools.chain(*[ss_elt for elt in Liste for ss_elt in zip(*elt)]))
    return liste_nettoyée


if __name__ == "__main__":
    # Définition des arguments
    liste_espece = ['Gallus gallus domesticus', 'Gasteracanthus cataphractus', 'Geboscon obliquum', 'Bergera koenigii']
    test = get_taxid(liste_espece)
    print(test)
