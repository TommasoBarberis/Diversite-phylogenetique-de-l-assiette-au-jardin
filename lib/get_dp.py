#  -*- coding: utf-8 -*-

from ete3 import Tree
import numpy as np
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

    species = list(species.values())
    tree = Tree(tree, format = 8, quoted_node_names = True)
    tree = tree.get_common_ancestor(species)
    
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

    species = list(species.values())
    tree = Tree(tree, format = 8, quoted_node_names = True)
    tree = tree.get_common_ancestor(species)
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
    Shannon's index with abundance in kg.
    """

    shannon = 0
    if len(species) == 0:
        shannon = "NA"
    else:
        denominator = 0
        print(dict_sp_drym)
        for c, sp in enumerate(species.values()):
            val = dict_sp_drym[sp][0] / 1000
            if c == 0:
                denominator = (val ** val)
            else:
                denominator *= (val ** val)
            
        shannon = round(np.log(1 / denominator), 2)
    return shannon


def simpson(species, dict_sp_drym):
    """
    Simpson's index with abundance in kg.
    """
    
    simpson = 0
    if len(species) == 0:
        simpson = "NA"
    else:
        for sp in species.values():
            simpson += (dict_sp_drym[sp][0] / 1000) ** 2

        simpson = round(simpson, 2)
    return simpson



if "__main__" == __name__:
    tree = "(((((((((((((((Piper nigrum)Piper)Piperaceae)Piperales)Magnoliidae,(((((((Allium sativum,Allium cepa)Allium)Allieae)Allioideae)Amaryllidaceae)Asparagales)Petrosaviidae)Liliopsida,(((((((((((((Daucus carota)Daucus sect. Daucus)Daucus)Daucinae)Scandiceae)Apioideae)Apiaceae)Apiineae)Apiales)campanulids)asterids)Pentapetalae)Gunneridae)eudicotyledons)Mesangiospermae)Magnoliopsida)Spermatophyta)Euphyllophyta)Tracheophyta)Embryophyta)Streptophytina)Streptophyta)Viridiplantae)Eukaryota);"
    ncbi = NCBITaxa()
    tree = ncbi.get_topology(([4679, 4682, 4039, 13216]), intermediate_nodes = True)
    tree = tree.write(format = 100, features = ["sci_name"]).replace('[&&NHX:sci_name=', '').replace(']', '')
    tree = Tree(tree, format = 8, quoted_node_names = True)
    nodes = tree.search_nodes()
    print(tree, "\n", nodes, "\n", len(nodes))
    ancestor = tree.get_common_ancestor("Piper nigrum", "Allium sativum", "Allium cepa", "Daucus carota")
    nodes = ancestor.search_nodes()
    # print(tree.get_common_ancestor())
    print(ancestor, "\n", nodes, "\n",len(nodes))
    # print(common_ancestor(tree))