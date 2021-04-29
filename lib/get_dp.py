#  -*- coding: utf-8 -*-

from collections import Counter


def length_root_to_knot (path):
  """Permet de construire un dictionnaire qui contient comme cle chaque noeud de l'arbre phylogenetique et comme valeur
  la distance en nb de branches entre la racine et le noeud.
  """
  f=open(path, "r", encoding="utf8")
  tree=f.read()
  tree = tree.replace('[', '').replace(']', '').replace("'", "").replace(';', '')
  dp = 0
  sp = ""
  c = 1
  iterator = 0
  dico_lengths = {}
  for ind,char in enumerate(tree):
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


def filter_dico_lengths (path,species):
  dico_lengths = length_root_to_knot(path)
  new_dico = {}
  for knot in dico_lengths.keys():
    if knot in species.values():
      new_dico[knot] = dico_lengths[knot]
  return new_dico


def phylogenetic_diversity (path, species):
  dico = filter_dico_lengths(path, species)
  pd = 0
  for i in dico:
    pd += dico[i]
  return pd


def weighted_phylogenetic_diversity (path, species, dict_sp_drym):
  dico = filter_dico_lengths(path, species)
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
