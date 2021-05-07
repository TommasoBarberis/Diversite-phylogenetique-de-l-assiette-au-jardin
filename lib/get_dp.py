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

def length_root_to_knot (tree):
  """
  Permet de construire un dictionnaire qui contient comme clé chaque noeud de l'arbre phylogenetique et comme valeur
  la distance en nb de branches entre la racine et le nœud a partir d'un arbre phylogénétique de Newick.
  """
  dp = 0
  sp = ""
  c = 1
  iterator = 0
  dico_lengths = {}
  for ind, char in enumerate(tree):
    if char == ",":
      c += 1
    if char == "(":
      iterator += 1
    elif char == ")" or char == ",":
      iterator -= 1
      if sp != "":
        dico_lengths[sp] = iterator + c
        sp = ""
    elif char != "(" and char != ")" and char != ",":
      sp += char
  return dico_lengths


def filter_dico_lengths (tree,species): 
  """
  Permet de créer un dictionnaire qui contient uniquement les espèces trouvées pour les ingrédients
  avec les longueurs (en nb de branches) noeud-racine calculées à partir de l'arbre phylogenetique de Newick.
  """
  dico_lengths = length_root_to_knot(tree)
  new_dico = {}
  for knot in dico_lengths.keys():
    if knot in species.values():
      new_dico[knot] = dico_lengths[knot]

  return new_dico


def phylogenetic_diversity (tree, species):
  # """
  # Ensuite à partir de ce dictionnaire on calcule la diversité phylogénétique de la recette en sommant
  # les longueurs des branches des espèces présentes dans le plat.
  # """
  # dico = filter_dico_lengths(tree, species)
  # pd = 0
  # for i in dico:
  #   pd += dico[i]
  
  tree = Tree(tree, format = 8, quoted_node_names = True)
  species = list(species.values())
  try:
    ancestor = tree.get_common_ancestor(species)
    nodes = ancestor.search_nodes()
    logger.info("The phylogenetic diversity of recipe as the number of nodes of the smallest tree containing all species is {}".format(str(len(nodes))))
  except:
    nodes = []
    logger.debug("Probably some species not have the same name in the tree and the species list, so it is impossible to compute the phylogentic diversity")
  return len(nodes)


def weighted_phylogenetic_diversity (tree, species, dict_sp_drym):
  dico = filter_dico_lengths(tree, species)
  wpd = 0
  for i in dico:
    try:
      wpd+=(int(dico[i])*int(dict_sp_drym[i]))
    except:
      wpd = "NA"
  sum_wight = 0
  if wpd != "NA":
    for i in dict_sp_drym.values():
      sum_wight += i
    wpd /= sum_wight
    wpd = '{0:.3g}'.format(wpd)
  return wpd


def common_ancestor(tree, node):
  ancestor = tree.get_common_ancestor(node)
  return ancestor


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