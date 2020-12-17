 # -*- coding: utf-8 -*-

import get_lifeMap_subTree
import get_ing
import ing_to_esp
import get_dp
import ing_properties
import os
import get_NCBI_taxonomy
from ete3 import NCBITaxa


url = input("Entrez l'url de la recette choisie. (préférence : Marmiton) \n") 
print("\n")
ingredients = get_ing.process(url)
especes = ing_to_esp.recherche_globale(ingredients)
dictionnaire_nutrition = ing_properties.getDictNut(ingredients)
nbing = len(ingredients)
nbspec = len(especes)
nbnut =len(dictionnaire_nutrition)
nut_not_found = []

def missing_species(ingredients, especes):
    species_not_found = []
    if nbing != nbspec :
        complete_spec = False
        for key in ingredients:
            if key not in especes and key[:-1] not in especes.keys():
                species_not_found.append(key)
    else : complete_spec = True
    return (species_not_found, complete_spec)


if nbing != nbnut :
    complete_nut = False
    for key in ingredients:
        if key.capitalize() not in dictionnaire_nutrition:
            nut_not_found.append(key.capitalize())
else : complete_nut = True

drym_dict = ing_properties.dryMatterDicUpdate(ingredients,dictionnaire_nutrition)
ing_properties.writeTsv("results.tsv",ingredients,especes,drym_dict,dictionnaire_nutrition)

list_ID = get_NCBI_taxonomy.get_taxid(especes)
ncbi=NCBITaxa()
tree=ncbi.get_topology((list_ID), intermediate_nodes=True)
tree=tree.write(format=100, features=["sci_name"]).replace('[&&NHX:sci_name=','').replace(']','')
try:
    os.remove("Tree.txt")
except :
    pass
with open("Tree.txt","w") as Tree:
    Tree.write(tree)

dp=get_dp.phylogenetic_diversity("Tree.txt", especes)    #diversite phylogenetique
var=missing_species(ingredients, especes)

dictionnaire_nutrition = ing_properties.getDictNut(ingredients)
drym_dict=ing_properties.dryMatterDicUpdate(ingredients, dictionnaire_nutrition)
dict_sp_drym={}
bool_var=True
for sp in especes.keys():
  if sp in drym_dict.keys():
    dict_sp_drym[especes[sp]]=drym_dict[sp]
  else:
    bool_var=False
    break
        
if bool_var==True:
  wdp=get_dp.weighted_phylogenetic_diversity("Tree.txt", especes, dict_sp_drym)  #diversite ponderee
else:
  wdp="NA"

######## printting part ########

print("\n" +str(nbspec)+ " species were found from the "+ str(nbing)+ " different ingredients.")

if not var[1] :
    print("the missing species are :")
    for missing in var[0]:
        print("\t" + missing)
        
print("\n" +str(nbnut)+ " ingredients were found in the nutrition database ,from the "+ str(nbing)+ " different ingredients.")
if not complete_nut :
    print("these ingredients are missing nutrition information :")
    for missing in nut_not_found:
        print("\t" + missing)

print("\n")

ing_properties.nutPrinter(dictionnaire_nutrition)

print("\ningredients :")
print(ingredients)
print("species :")
print(especes)
print("dry matter :")
print(drym_dict)
get_lifeMap_subTree.get_newick(especes)
print("Diversité phylogénétique :")
print(dp)
print("Diversité phylogénétique pondérée:")
print(wdp)
print("All results were saved in the results.tsv file.")
