#  -*- coding: utf-8 -*-

from ete3 import Tree
import numpy as np
import lib.get_lifeMap_subTree as lm
import logging

logger = logging.getLogger("get_dp.py")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def phylogenetic_diversity (tree, species):
    """
    Calcul de la diversite phylogenetique a aprtir de la topologie de l'arbre taxonomique des especes presentes
    dans la recette avec la metrique MDP proposee par Webb en 2002.
    """

    species = list(filter(("NA").__ne__, species.values()))
    for sp in species:
        sp_id = lm.get_taxid({"key": sp})
        if sp_id == []:
            species.remove(sp)

    tree = Tree(tree, format = 8, quoted_node_names = True)
    try:
        tree = tree.get_common_ancestor(species)
    except Exception as ex:
        logger.exception(ex)
        return "NA"
    
    pd = 0 # phylogenetic diversity

    if len(species) == 0:
        pd = "NA"
    elif len(species) == 1:
        pd = 1
    else:
        for sp in species:

            mpd = 0 # mean pairwise distance

            for leaf in species:
                if sp == leaf:
                    pass
                else:
                    mpd += tree.get_distance(sp, leaf)
            
            mpd /= (len(species) - 1)
            pd += mpd

    logger.info("The MPD for this recipe is {}".format(pd))
    return round(pd, 2)


def weighted_phylogenetic_diversity(tree, species, dict_sp_drym):
    """
    Calcul de la diversite phylogenetique ponderee a aprtir de la topologie de l'arbre taxonomique des especes
     presentes dans la recette avec la metrique MDP proposee par Webb en 2002, en utilisant les quantites de 
     matiere seche.
    """
    del_sp = [] # it allows to delete species whose taxaid isn't found
    for ing in species:
        sp_id = lm.get_taxid({"ing": species[ing]})
        if sp_id == []:
            del_sp.append(ing)
    for ing in del_sp:
        del species[ing]

    species_list = list(filter(("NA").__ne__, species.values()))    

    tree = Tree(tree, format = 8, quoted_node_names = True)
    try:
        tree = tree.get_common_ancestor(species_list)
    except Exception:
        logger.exception("Some species are not found")
        return "NA"
    

    wpd = 0 # weighted phylogenetic diversity

    if len(species) == 0:
        wpd = "NA"
    elif len(species) == 1:
        for sp in species:
            wpd = dict_sp_drym[species[ing]][0]
    else:        
        weight_sum = 0
        for ing in species:

            mpd = 0 # mean pairwise distance

            for leaf in species_list:
                if species[ing] != leaf:
                    mpd += tree.get_distance(species[ing], leaf)
            
            try:
                weight = float(dict_sp_drym[species[ing]][0])
            except Exception:
                logger.exception("The ingredients '{}' has not a valid quantity of dry matter".format(ing))
                return "NA"
            mpd = (mpd / (len(species) - 1)) * weight
            weight_sum += weight
            wpd += mpd
        
        wpd /= weight_sum

    logger.info("The weighted MPD for this recipe is {}".format(wpd))
    return round(wpd, 2)


def shannon(species, dict_sp_drym):
    """
    Shannon's index with abundance in hg.
    """
    species = list(filter(("NA").__ne__, species.values()))
    shannon = 0
    if len(species) == 0:
        shannon = "NA"
    else:
        denominator = 0
        for c, sp in enumerate(species):
            try:
                val = dict_sp_drym[sp][0] / 100
            except:
                logger.info("Impossible compute Shannon's index because the ingredient '{}' has not a dry matter quantity".format(sp))
                return "NA"
            if c == 0:
                denominator = (val ** val)
            else:
                denominator *= (val ** val)
            
        shannon = round(np.log(1 / denominator), 2)
    return shannon


def simpson(species, dict_sp_drym):
    """
    Simpson's index with abundance in hg.
    """
    species = list(filter(("NA").__ne__, species.values()))
    simpson = 0
    if len(species) == 0:
        simpson = "NA"
    else:
        for sp in species:
            try:
                simpson += (dict_sp_drym[sp][0] / 100) ** 2
            except:
                logger.info("Impossible compute Simpson's index because the ingredient '{}' has not a dry matter quantity".format(sp))
                return "NA"


        simpson = round(simpson, 2)
    return simpson



if "__main__" == __name__:
    tree = "(((((((((((((((Piper nigrum)Piper)Piperaceae)Piperales)Magnoliidae,(((((((Allium sativum,Allium cepa)Allium)Allieae)Allioideae)Amaryllidaceae)Asparagales)Petrosaviidae)Liliopsida,(((((((((((((Daucus carota)Daucus sect. Daucus)Daucus)Daucinae)Scandiceae)Apioideae)Apiaceae)Apiineae)Apiales)campanulids)asterids)Pentapetalae)Gunneridae)eudicotyledons)Mesangiospermae)Magnoliopsida)Spermatophyta)Euphyllophyta)Tracheophyta)Embryophyta)Streptophytina)Streptophyta)Viridiplantae)Eukaryota);"
    ncbi = NCBITaxa()