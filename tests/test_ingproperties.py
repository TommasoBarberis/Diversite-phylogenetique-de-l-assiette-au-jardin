import sys 
import os
import lib.ing_properties as ip
import lib.get_ing as gi
import xlrd


def test_getNutInfo():
    file_path = "data/Table_Ciqual_2020_FR_2020_07_07.xls"
    book = xlrd.open_workbook(file_path)
    ing = "Poivre"
    assert len(ip.getNutInfo(ing, book)) == 5

def test_dryMatterDicUpdate():
    ingredients = gi.process("https://www.marmiton.org/recettes/recette_tartiflette-en-gratin_529817.aspx")
    dict_nut = ip.getDictNut(ingredients)
    dry_matter = ip.dryMatterDicUpdate(ingredients, dict_nut)
    for ing in dry_matter:
        assert (float(dry_matter[ing][0]) < float(ingredients[ing][1]))
