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

    species = list(filter(("-").__ne__, species.values()))
    for sp in species:
        sp_id = lm.get_taxid({"key": sp})
        if sp_id == []:
            species.remove(sp)

    tree = Tree(tree, format = 8, quoted_node_names = True)
    try:
        tree = tree.get_common_ancestor(species)
    except Exception as ex:
        logger.exception("Some species are not found" + ex)
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

    species = list(filter(("-").__ne__, species.values()))
    for sp in species:
        sp_id = lm.get_taxid({"key": sp})
        if sp_id == []:
            species.remove(sp)

    tree = Tree(tree, format = 8, quoted_node_names = True)
    try:
        tree = tree.get_common_ancestor(species)
    except Exception:
        logger.exception("Some species are not found")
        print("return in except")
        return "NA"
        
    wpd = 0 # weighted phylogenetic diversity

    if len(species) == 0:
        wpd = "NA"
    elif len(species) == 1:
        for sp in species:
            wpd = dict_sp_drym[sp][0]
    else:        
        weight_sum = 0
        for sp in species:

            mpd = 0 # mean pairwise distance

            for leaf in species:
                if sp != leaf:
                    mpd += tree.get_distance(sp, leaf)
            
            weight = dict_sp_drym[sp][0]
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
    species = list(filter(("-").__ne__, species.values()))
    shannon = 0
    if len(species) == 0:
        shannon = "NA"
    else:
        denominator = 0
        for c, sp in enumerate(species):
            val = dict_sp_drym[sp][0] / 100
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
    species = list(filter(("-").__ne__, species.values()))
    simpson = 0
    if len(species) == 0:
        simpson = "NA"
    else:
        for sp in species:
            simpson += (dict_sp_drym[sp][0] / 100) ** 2

        simpson = round(simpson, 2)
    return simpson



if "__main__" == __name__:
    tree = "(((((((((((((((Piper nigrum)Piper)Piperaceae)Piperales)Magnoliidae,(((((((Allium sativum,Allium cepa)Allium)Allieae)Allioideae)Amaryllidaceae)Asparagales)Petrosaviidae)Liliopsida,(((((((((((((Daucus carota)Daucus sect. Daucus)Daucus)Daucinae)Scandiceae)Apioideae)Apiaceae)Apiineae)Apiales)campanulids)asterids)Pentapetalae)Gunneridae)eudicotyledons)Mesangiospermae)Magnoliopsida)Spermatophyta)Euphyllophyta)Tracheophyta)Embryophyta)Streptophytina)Streptophyta)Viridiplantae)Eukaryota);"
    ncbi = NCBITaxa()