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

dry_matter_dict = ing_properties.dryMatterDicUpdate(ingredients,dictionnaire_nutrition)
ing_properties.writeTsv("new.tsv",ingredients,especes,dry_matter_dict,dictionnaire_nutrition)

######## printting part ########

print("\n" +str(nbspec)+ " species were found from the "+ str(nbing)+ " different ingredients.")

var=missing_species(ingredients, especes)
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
print(dry_matter_dict)
get_lifeMap_subTree.get_newick(especes)
print("Diversité phylogénétique (en nb de branches) :")
dp=get_dp.calculation("Tree.txt")
print(dp)
get_lifeMap_subTree.subtree_from_newick()