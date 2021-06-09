#  -*- coding: utf-8 -*-

# import urllib3
import bs4 #import BeautifulSoup
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


def get_cuisinelibre(soup):
    ingredients = {}
    list_unit = ["mg", "g", "dag", "hg", "kg", "ml", "cl", "dl", "l"]
    try:
        list_ing = soup.findAll("li", {"class": "ingredient"})
        # print(list_ing)
        for li in list_ing:
            qty = "NA"
            unit = ["", ""]

            li_text = li.get_text()
            li_text = li_text.split(" ")
            li_text = li_text[1:]
            if li_text[0].isnumeric():
                qty = float(li_text[0].replace(",", "."))
                if li_text[1] in list_unit:
                    unit = [li_text[1], li_text[1]]
                    del li_text[1]
                else:
                    for unit_mass in list_unit:
                        if unit_mass in li_text:
                            index_unit = li_text.index(unit_mass)
                            f = float(li_text[index_unit-1].replace(",", "."))
                            qty = qty * f
                            # qty = qty * float(li_text[index_unit-1].replace(",", "."))
                            unit = [unit_mass, unit_mass]
                            del li_text[index_unit]
                            del li_text[index_unit-1]
                del li_text[0]
            
            clean_list = ["de", "des"]
            if li_text[0] in clean_list:
                del li_text[0]
            if li_text[-1] in clean_list:
                del li_text[-1]
            

            
                
            print(li_text, qty, unit)
    except Exception:
        logger.exception("Error in ingredient parsing")


def get_marmiton(soup):
    ingredients = {}
    ingredients = ing_complete(soup, ingredients)
    return ingredients
    # # First parser
    # try:
    #     html_ingredients_list = soup.findAll("div", {"class": "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-4 MuiGrid-grid-sm-3"}) # select html tag with this class in recipe web page
    #     for i in html_ingredients_list:
        
    #         first_level = i.find("div")
    #         info_div = first_level.findAll("div")[1]
    #         qty_unit_span = info_div.find("span")
    #         qty_unit_span = qty_unit_span.get_text().replace(u'\xa0', ' ')
            
    #         if qty_unit_span == '':
    #             qty = "NA"
    #             unit = ["", ""]
    #         else:
    #             c = 0 # counter
    #             qty = ""

    #             while True:
    #                 if qty_unit_span[c] == " ":
    #                     break
    #                 else:
    #                     qty += qty_unit_span[c]
    #                     c += 1
                
    #             unit = qty_unit_span[c+1:len(qty_unit_span)]
    #             unit = [unit, unit]

    #         ing_span = first_level.findAll("span")[1]
    #         ing_span = ing_span.get_text()
    #         ing = [ing_span, ing_span]

    #         val = [ing, qty, unit]
    #         ingredients[ing[0]] = val

    #     ingredients = search_in_default_mass(ingredients)
            
    #     assert len(ingredients) != 0
    #     for ing in ingredients:
    #         if ing.isnumeric():
    #             del ingredients[ing]    
    #     logger.debug("Ingredient parsing, parser 1, DONE")
    #     return ing_complete(soup, ingredients)
    # except Exception:
    #     logger.exception("Error in ingredient parsing, parser 1 failed")
    
    # # Second parser
    # try:
    #     html_ingredients_list = soup.find("div", {"class": "ingredient-list__ingredient-group"}) # select html tag with this class in recipe web page
    #     li_tags = html_ingredients_list.findAll("li") # object with all ingredients and quantities for the recipe
        
    #     for i in range(0,len(li_tags)):
    #         ing = [li_tags[i].find("div", {"class": "ingredient-data"}).get("data-singular"), li_tags[i].find("div", \
    #             {"class": "ingredient-data"}).get("data-plural")]
    #         qty = li_tags[i].find("div", {"class": "quantity-data"}).get_text()
    #         unit = [li_tags[i].find("div", {"class": "unit-data"}).get("data-singular"), li_tags[i].find("div", \
    #             {"class": "unit-data"}).get("data-plural")]
    #         val = [ing, qty, unit]
    #         ingredients[li_tags[i].find("div", {"class": "ingredient-data"}).get("data-singular")] = val

    #     ingredients = search_in_default_mass(ingredients)

    #     assert len(ingredients) != 0
    #     for ing in ingredients:
    #         if ing.isnumeric():
    #             del ingredients[ing]    
    #     logger.debug("Ingredient parsing, parser 2, DONE")
    #     return ing_complete(soup, ingredients)
    # except Exception:
    #     logger.exception("Error in ingredient parsing, parser 2 failed")

    # # Third parser
    # try:
    #     html_ingredients_list = soup.findAll("div", {"class": "MuiGrid-root MuiGrid-item MuiGrid-grid-xs-4 MuiGrid-grid-md-3"}) # select html tag with this class in recipe web page

    #     for i in html_ingredients_list:
    #         first_level = i.find("div")
    #         info_div = first_level.findAll("div")[1]

    #         qty_unit_span = info_div.find("span")
    #         qty_unit_span = qty_unit_span.get_text().replace(u'\xa0', ' ').replace(' ', '*')

    #         if qty_unit_span == '':
    #             qty = "NA"
    #             unit = ["", ""]
    #         else:
    #             qty_unit_span = qty_unit_span.split("*")
    #             qty = qty_unit_span[0]
    #             unit = [qty_unit_span[1], qty_unit_span[1]]

    #         ing_span = first_level.findAll("span")[1]
    #         ing_span = ing_span.get_text().replace(u'\xa0', '')
    #         ing = [ing_span, ing_span]

    #         val = [ing, qty, unit]
    #         ingredients[ing[0]] = val

    #     ingredients = search_in_default_mass(ingredients)

    #     assert len(ingredients) != 0  
    #     logger.debug("Ingredient parsing, parser 3, DONE")
    #     return ing_complete(soup, ingredients)
    # except Exception:
    #     logger.exception("Error in ingredient parsing, parser 3 failed")

def ing_complete(soup, ingredients):
    new_dict = {}
    for ing in ingredients:
        if ing != "" and ing.isnumeric() == False:
            new_dict[ing] = ingredients[ing]
    ingredients = new_dict

    try:
        og_description = soup.findAll("meta", {"property": "og:description"})
        ing_list = og_description[0]["content"].split(", ")

        for ing in ing_list:
            pl = ing + "s"
            if ing.capitalize() not in ingredients.keys() and pl.capitalize() not in ingredients.keys():
                ingredients[ing.capitalize()] = [[ing, ing], "NA", ["", ""]]
    except:
        pass
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
