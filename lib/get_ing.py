#  -*- coding: utf-8 -*-

import bs4
import requests
from urllib.parse import urlparse
import re
import sys
from difflib import SequenceMatcher
import logging

logger = logging.getLogger("get_ing.py")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def process(url):
    req = requests.get(url)
    domain = urlparse(url).netloc
    soup = bs4.BeautifulSoup(req.content, 'html.parser')
    if domain == "www.marmiton.org":   
        ingredients = get_marmiton(soup)
        return ingredients
    if domain == "www.cuisine-libre.org":
        ingredients = get_cuisinelibre(soup)
        return ingredients
    print("err: invalid domain, please take a recipe from marmiton.org")
    logger.error("{} has invalid domain".format(url))


def get_title(url):
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.content, 'html.parser')

    # First parser
    try:
        html_title = soup.find("main").find("h1").get_text()
        logger.debug(html_title)
        return html_title
    except:
        html_title = "\tRecipe title not found"
        
    # Second parser
    try:
        html_title = soup.findAll("h1",{"class":'main-title show-more'})
        html_title = html_title[0].get_text()
        logger.debug(html_title)
        return html_title
    except:
        html_title = "\tRecipe title not found"

    # Third parser
    try:
        html_title = soup.find("title")
        html_title = html_title.split(":")[0]
        return html_title
    except:
        html_title = "\tRecipe title not found"

    return html_title


def search_in_default_mass(ingredients):
    for ing in ingredients:
        if ingredients[ing][2][1] == "" and (ingredients[ing][1] != '' and ingredients[ing][1] != "NA"):
            with open("filtering/default_mass.txt", "r") as f:
                lines = f.readlines() # file that allow to get mass for some ingredients
        
                for line in lines:
                    ing_mass = line.split("/")
                    if ing.capitalize() == ing_mass[0]:

                        number = ingredients[ing][1]
                        try:
                            qty = int(number) * int(ing_mass[1].replace("\n", ""))
                            ingredients[ing] = [[ing, ing], str(qty), ["g", "g"]]
                        except:
                            pass
    return ingredients


def get_marmiton(soup):
    ingredients = {}
    try:
        og_description = soup.findAll("meta", {"property": "og:description"})
        ing_list = og_description[0]["content"].split(", ")

        for ing in ing_list:
            pl = ing + "s"
            if ing.capitalize() not in ingredients.keys() and pl.capitalize() not in ingredients.keys():
                ingredients[ing.capitalize()] = [[ing, ing], "NA", ["", ""]]
    except Exception:
        ingredients = None
        logger.exception("Error in parsing")
    return ingredients



if __name__ == "__main__":
  

    url = "https://www.marmiton.org/recettes/recette_bruschetta-a-la-mozzarella_30276.aspx"
   
    from urllib import request
    res = request.urlopen(url).read()
    # res est de type bytes, il faut le convertir
    page = res.decode("utf8")
    start_title = page.find("<title>") + len("<title>")
    end_title = page.find("</title>")
    title = page[start_title:end_title]
    
    import re
    match = re.search("title>.*?</title", page)
    print(match)
    # print(process("https://www.marmiton.org/recettes/recette_bruschetta-a-la-mozzarella_30276.aspx"))
