import lib.get_ing as gi 
import bs4
import requests
from urllib.parse import urlparse


def test_process():
    url = "https://www.marmiton.org/recettes/recette_tartiflette-en-gratin_529817.aspx"
    ingredients = gi.process(url)
    assert isinstance(ingredients, dict)


def test_getTitle():
    title = gi.get_title("https://www.marmiton.org/recettes/recette_tartiflette-en-gratin_529817.aspx")
    assert type(title) is str


def test_searchDefaultMass():
    ingredients = {'poivre': [['poivre', 'poivre'], 'NA', ['pincée', 'pincées']]}
    new_ingredients = gi.search_in_default_mass(ingredients)
    assert ingredients == new_ingredients
    ingredients = {'poivre': [['poivre', 'poivre'], '', ['pincée', 'pincées']]}
    new_ingredients = gi.search_in_default_mass(ingredients)
    assert ingredients == new_ingredients
    ingredients = {'poivre': [['poivre', 'poivre'], '1', ['pincée', 'pincées']]}
    new_ingredients = gi.search_in_default_mass(ingredients)
    assert ingredients == new_ingredients
    ingredients = {'poivre': [['poivre', 'poivre'], '1', ['', '']]}
    new_ingredients = gi.search_in_default_mass(ingredients)
    assert isinstance(new_ingredients, dict)


def test_getMarmiton():
    url = "https://www.marmiton.org/recettes/recette_tartiflette-en-gratin_529817.aspx"
    req = requests.get(url)
    domain = urlparse(url).netloc
    soup = bs4.BeautifulSoup(req.content, 'html.parser')
    ingredients = gi.get_marmiton(soup)

    assert isinstance(ingredients, dict)
