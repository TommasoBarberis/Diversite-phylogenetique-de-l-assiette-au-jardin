#  -*- coding: utf-8 -*-

from lib import get_lifeMap_subTree, get_ing, ing_to_esp, get_dp, ing_properties, get_NCBI_taxonomy
import os
from ete3 import NCBITaxa
import logging


logger = logging.getLogger("main.py")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# url input
url = input("Enter the url recipe. (from Marmiton.org) \n") 
print("\n")
logger.info("URL recipe entered by user: " + url)


# getting ingredients from web site
try:
    ingredients = get_ing.process(url)
    logger.info("Parsing of ingredients, DONE")
except Exception:
    logger.exception("Error in parsing ingredients")

# getting species
try:
    especes = ing_to_esp.recherche_globale(ingredients)
    logger.info("Conversion of ingredients in species, DONE")
except Exception:
    logger.exception("Error in conversion of ingredients to species")

try:
    dictionnaire_nutrition = ing_properties.getDictNut(ingredients)
    logger.info("Get nutritional information, DONE")
except Exception:
    logger.exception("Error in getting nutritional information")

nbing = len(ingredients)
nbspec = len(especes)
nbnut = len(dictionnaire_nutrition)
nut_not_found = []

def missing_species(ingredients, especes):
    species_not_found = []
    if nbing != nbspec :
        complete_spec = False
        for key in ingredients:
            if key not in especes and key[:-1] not in especes.keys():
                species_not_found.append(key)
    else:
        complete_spec = True
    return (species_not_found, complete_spec)

if nbing != nbnut :
    complete_nut = False
    for key in ingredients:
        if key.capitalize() not in dictionnaire_nutrition:
            nut_not_found.append(key.capitalize())
else:
    complete_nut = True

try:
    drym_dict = ing_properties.dryMatterDicUpdate(ingredients, dictionnaire_nutrition)
    logger.info("Process the quantity of dry matter of ingredients, DONE")
except Exception:
    logger.exception("Error in processing quantity of dry matter")


try:
    ing_properties.writeTsv("results.tsv", ingredients, especes, drym_dict, dictionnaire_nutrition)
    logger.info("Sum-up of informations in a .tsv file, DONE")
except Exception:
    logger.exception("Error in writing .tsv")

try:
    list_ID = get_NCBI_taxonomy.get_taxid(especes)
    logger.info("Get taxa id of species, DONE")
except Exception:
    logger.exception("Error in getting taxa id")

try:
    ncbi = NCBITaxa()
    logger.info("Download and parse the latest database from the NCBI ftp site, DONE")
except Exception:
    logger.exception("Error in download NCBI database")

try:
    tree = ncbi.get_topology((list_ID), intermediate_nodes=True)
    tree = tree.write(format=100, features=["sci_name"]).replace('[&&NHX:sci_name=', '').replace(']', '')
    try:
        os.remove("Tree.txt")
    except Exception:
        pass
    with open("Tree.txt", "w") as Tree:
        Tree.write(tree)
    logger.info("Tree construction, DONE")
except Exception:
    logger.exception("Error in tree construction")


# computation of the phylogenetic diversity
try:
    dp = get_dp.phylogenetic_diversity("Tree.txt", especes) # phylogenetic diversity
    logger.info("computation of the phylogenetic diversity, DONE")
except Exception:
    logger.exception("Error in phylogenetic diversity computation")

# find the missing species for ingredients
try:
    var = missing_species(ingredients, especes)
    logger.info("Missing species, DONE")
except Exception:
    logger.exception("Error in detection of missing species")

# computation of weighted phylogenetic diversity
try:
    dict_sp_drym = {}
    bool_var = True
    for sp in especes.keys():
        if sp in drym_dict.keys():
            dict_sp_drym[especes[sp]] = drym_dict[sp]
        else:
            bool_var = False
            break

    if bool_var is True:
        wdp = get_dp.weighted_phylogenetic_diversity("Tree.txt", especes, dict_sp_drym)  # weighted phylogenetic diversity
    else:
        wdp = "NA"
    logger.info("Computation of weighted phylogenetic diversity, DONE")
except Exception:
    logger.exception("Error in weighted phylogenetic diversity computation")

print("\n" + str(nbspec) + " species were found from the " + str(nbing) + " different ingredients.")

if not var[1]:
    print("the missing species are :")
    for missing in var[0]:
        print("\t" + missing)

print("\n" + str(nbnut) + " ingredients were found in the nutrition database ,from the " + str(nbing) \
    + " different ingredients.")
if not complete_nut:
    print("these ingredients are missing nutrition information :")
    for missing in nut_not_found:
        print("\t" + missing)

print("\n")

ing_properties.nutPrinter(dictionnaire_nutrition)

print("\ningredients :")
ingredients_list = []
for ing in ingredients.keys():
    ingredients_list.append(ing)
print(ingredients_list)
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


# keep only last 1000 lines of the log file
try:
    with open("log.txt", "r") as log:
        lines = log.readlines()
        log_length = len(lines)
        if log_length > 1000:
            lines = lines[(log_length-1001):-1]

    with open("log.txt", "w") as log:
        for line in lines:
            log.write(line) 
finally:
    pass
