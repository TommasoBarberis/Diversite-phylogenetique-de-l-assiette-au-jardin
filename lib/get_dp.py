#  -*- coding: utf-8 -*-

from collections import Counter
from ete3 import Tree, NCBITaxa
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
    dans la recette avec la metrique MDP proposee par .....
    """
    # """
    # Ensuite à partir de ce dictionnaire on calcule la diversité phylogénétique de la recette en sommant
    # les longueurs des branches des espèces présentes dans le plat.
    # """
    # dico = filter_dico_lengths(tree, species)
    # pd = 0
    # for i in dico:
    #   pd += dico[i]

    pd = "NA" # phylogenetic diversity

    tree = Tree(tree, format = 8, quoted_node_names = True)
    species = list(species.values())
    tree = tree.get_common_ancestor(species)
    nodes = tree.search_nodes()

    for sp in species:

        sum_dist = 0

        for leaf in species:
            if sp == leaf:
                pass
            else:
                sum_dist += tree.get_distance(sp, leaf)
    
        # print(sum_dist/(len(species)-1))

    return pd




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