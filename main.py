 # -*- coding: utf-8 -*-

# import get_lifeMap_subTree
import get_ing
import ing_to_esp
import get_dp
import ing_properties

print("\n")

url = 'https://www.marmiton.org/recettes/recette_poke-bowl-avocat-et-thon-marine_344612.aspx'
ingredients = get_ing.process(url)
especes = ing_to_esp.recherche_globale(ingredients)
nbing = len(ingredients)
nbspec = len(especes)
species_not_found = []
if nbing != nbspec :
    complete = False
    for key in ingredients:
        if key not in especes and key[:-1] not in especes.keys():
            species_not_found.append(key)

dp=get_dp.calculation("exemple_newick.txt")
dictionnaire_nutrition = ing_properties.getDictNut(ingredients)

######## printting part ########

print("\n" +str(nbspec)+ " species were found from the "+ str(nbing)+ " different ingredients.")
if not complete :
    print("the missing species are :")
    for missing in species_not_found:
        print("\t" + missing)
ing_properties.nutPrinter(dictionnaire_nutrition)

print("\ningredients :")
print(ingredients)
print("species :")
print(especes)
print("Diversité phylogénétique (en nb de branches) :")
print(dp)
