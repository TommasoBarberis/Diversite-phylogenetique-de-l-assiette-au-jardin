import sys 
import os
import lib.ing_properties as ip
import lib.get_ing as gi
import xlrd

def test_openBook():
    filename = "data/Table_Ciqual_2020_FR_2020_07_07.xls"
    book = ip.open_book(filename)
    assert isinstance(book, xlrd.book.Book)


def test_getDefaultLineNumber():
    ing = "sel"
    line = ip.get_default_line_number(ing)
    assert line == 3040


def test_getNutInfo():
    file_path = "data/Table_Ciqual_2020_FR_2020_07_07.xls"
    book = xlrd.open_workbook(file_path)
    ing = "Poivre"
    assert len(ip.get_nut_info(ing, book)) == 5


def test_getDictNut():
    dict_ing = {'farine': [['farine', 'farine'], '40', ['g', 'g']], 'poire': [['poire', 'poires'], '3', ['', '']], 'beurre': [['beurre', 'beurre'], '60', ['g', 'g']]}
    dict_nut = ip.get_dict_nut(dict_ing)
    assert isinstance(dict_nut, dict)
    assert len(dict_nut) == len(dict_ing)    


def test_dryMatterDicUpdate():
    ingredients = gi.process("https://www.marmiton.org/recettes/recette_tartiflette-en-gratin_529817.aspx")
    dict_nut = ip.get_dict_nut(ingredients)
    dry_matter = ip.dry_matter_dict_update(ingredients, dict_nut)
    for ing in dry_matter:
        if dry_matter[ing][0] != "-": # if a dry matter quantity is not found, skip the test
            assert (float(dry_matter[ing][0]) < float(ingredients[ing][1]))


def test_formatFloat():
    string1 ="ing1-ing2"
    resultat = ip.format_float(string1)
    assert resultat == 0

    string2 = "traces"
    resultat = ip.format_float(string2)
    assert resultat == 0

    string3 = "34 < 4"
    resultat = ip.format_float(string3)
    assert "< " not in resultat

    string4 = "3,2"
    resultat = ip.format_float(string4)
    assert "," not in resultat
    assert "." in resultat