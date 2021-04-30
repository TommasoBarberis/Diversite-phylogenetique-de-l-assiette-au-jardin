import lib.get_ing as gi 

def test_get_title():
    title = gi.get_title("https://www.marmiton.org/recettes/recette_tartiflette-en-gratin_529817.aspx")
    assert type(title) is str



