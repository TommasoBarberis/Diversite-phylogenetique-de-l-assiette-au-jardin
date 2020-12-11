 # -*- coding: utf-8 -*-

import get_lifeMap_subTree
import get_ing
import ing_to_esp
import get_dp
import ing_properties
import os

url = input("Entrez l'url de la recette choisie. (préférence : Marmiton) \n") 
print("\n")
ingredients = get_ing.process(url)
especes = ing_to_esp.recherche_globale(ingredients)
dictionnaire_nutrition = ing_properties.getDictNut(ingredients)
nbing = len(ingredients)
nbspec = len(especes)
nbnut =len(dictionnaire_nutrition)
species_not_found = []
nut_not_found = []

if nbing != nbspec :
    complete_spec = False
    for key in ingredients:
        if key not in especes and key[:-1] not in especes.keys():
            species_not_found.append(key)
else : complete_spec = True

if nbing != nbnut :
    complete_nut = False
    for key in ingredients:
        if key.capitalize() not in dictionnaire_nutrition:
            nut_not_found.append(key.capitalize())
else : complete_nut = True


######## printting part ########

print("\n" +str(nbspec)+ " species were found from the "+ str(nbing)+ " different ingredients.")

if not complete_spec :
    print("the missing species are :")
    for missing in species_not_found:
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
get_lifeMap_subTree.get_newick(especes)
print("Diversité phylogénétique (en nb de branches) :")
dp=get_dp.calculation("Tree.txt")
print(dp)
get_lifeMap_subTree.subtree_from_newick()
