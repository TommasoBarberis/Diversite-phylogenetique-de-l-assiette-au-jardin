#  -*- coding: utf-8 -*-

# import urllib3
import bs4 #import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import sys
from difflib import SequenceMatcher


def process(url):
    req = requests.get(url)
    domain = urlparse(url).netloc
    soup = bs4.BeautifulSoup(req.content, 'html.parser')
    if domain == "www.marmiton.org":   
        ingredients = get_marmiton(soup)
    return ingredients


def get_title(url):
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.content, 'html.parser')
    html_title = soup.findAll("h1", {"class": 'main-title'})
    try:
        string_title = html_title[0].get_text()
        string_title = re.sub('\s+',' ',string_title) # se débarasse des \t et \n
    except:
        string_title = "\tRecipe title not found"
    return string_title


def get_marmiton(soup):

    ingredients = {}

    html_title = soup.findAll("h1",{"class":'main-title'}) 
    string_title = html_title[0].get_text()
    string_title = re.sub('\s+',' ',string_title) # se débarasse des \t et \n 

    html_ingredients_list = soup.find("div", {"class": "ingredient-list__ingredient-group"}) # select html tag with this class in recipe web page
    li_tags = html_ingredients_list.findAll("li") # object with all ingredients and quantities for the recipe

    for i in range(0,len(li_tags)):
        ing = [li_tags[i].find("div", {"class": "ingredient-data"}).get("data-singular"), li_tags[i].find("div", \
            {"class": "ingredient-data"}).get("data-plural")]
        qty = li_tags[i].find("div", {"class": "quantity-data"}).get_text()
        unit = [li_tags[i].find("div", {"class": "unit-data"}).get("data-singular"), li_tags[i].find("div", \
            {"class": "unit-data"}).get("data-plural")]
        val = [ing, qty, unit]
        ingredients[li_tags[i].find("div", {"class": "ingredient-data"}).get("data-singular")] = val
    return ingredients


if __name__ == "__main__":

    url = 'https://www.marmiton.org/recettes/recette_pizza-gaufree-au-fromage_347268.aspx'
    print(get_title(url))
    print(process("https://www.marmiton.org/recettes/recette_bruschetta-a-la-mozzarella_30276.aspx"))