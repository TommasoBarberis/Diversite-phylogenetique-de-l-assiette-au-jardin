import lib.ing_properties as ip
import lib.get_ing as gi


def test_getNutInfo():
    book = ip.openBook("../data/Table_Ciqual_2020_FR_2020_07_07.xls")
    ing = "Poivre"
    assert len(ip.getNutInfo(ing, book)) == 5

def test_dryMatterDicUpdate():
    ingredients = gi.process("https://www.marmiton.org/recettes/recette_tartiflette-en-gratin_529817.aspx")
    dict_nut = ip.getDictNut(ingredients)
    dry_matter = ip.dryMatterDicUpdate(ingredients, dict_nut)
    for ing in dry_matter:
        assert (dry_matter[ing][0] < ingredients[ing][1])
