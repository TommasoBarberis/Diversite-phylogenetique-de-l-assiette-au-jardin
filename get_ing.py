# import urllib3
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import sys
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def cleanAndPonderate(ing_comp_input):
    similarity_threshold = 0.8
    ing_comp_output = ing_comp_input.copy()
    f = open("filtering/ing_filter_start.txt", "r")
    elem_list_start = f.read().splitlines()
    f2 = open("filtering/ing_filter_end.txt", "r")
    elem_list_end = f2.read().splitlines()
    ingredient  = ing_comp_input[0]
    for line in elem_list_start:
        values = line.split("/")
        if ingredient.startswith(values[0]):
            ingredient = ingredient[len(values[0]):]
            if len(values) >1 :
                ing_comp_output[1] *= int(values[1])
                ing_comp_output[2] = "True"

    if not ing_comp_output[2]:
        f3 = open("filtering/default_mass.txt", "r")
        default_mass_list = f3.read().splitlines()
        for ing in default_mass_list :
            ingandmass = ing.split("/")
            score = similar(ingandmass[0].lower(),ing_comp_input[0])
            if score >= similarity_threshold :
                ing_comp_output[1] *= float(ingandmass[1])
                ing_comp_output[2] = "True"
                break
                
                
            
    for line in elem_list_end:
        if ingredient.endswith(line) :
            ingredient = ingredient[:len(line)]
    ing_comp_output[0] = ingredient
    return ing_comp_output

#base units : g 
def get_ing_only (ing_line):
    ing_comp =['',1,False] # format : ["name", "quantity" , "ponderable"]
    ing_comp[0]= ing_line.lower()

    #remove space before number
    if ing_comp[0].startswith(' ') :
        ing_comp[0]= ing_comp[0][1:]
    
    #enlève la quantité si elle est présente au début de la ligne
    temp = re.findall(r'\d+', ing_comp[0]) 
    res = list(map(int, temp))
    if res != [] : 
        ing_comp[0] = ing_comp[0][(len(str(res[0]))):]
        ing_comp[1] = res[0]
        if ing_comp[0].startswith(',') :
            ing_comp[0] = ing_comp[0][(len(str(res[1]))+1):]
            ing_comp[1] = ing_comp[1] + res[1]*0.1
            
    #remove space after number
    if ing_comp[0].startswith(' ') :
        ing_comp[0] = ing_comp[0][1:]
        
    output = cleanAndPonderate(ing_comp)
    
    return output

def process(url):

    req = requests.get(url)
    domain = urlparse(url).netloc
    soup = BeautifulSoup(req.content, 'html.parser')
    if domain == "www.marmiton.org" :   
        ingredients = getMarmiton(soup)
    elif domain == "www.750g.com" :
        ingredients = get750g(soup)
    elif domain == "www.cuisineaz.com" :
        ingredients = getCuisineaz(soup)
    else :
        #print("Invalid domain")
        sys.exit(1)
    
    return ingredients

def get_title(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    html_title = soup.findAll("h1",{"class":'main-title'})
    try:
        string_title = html_title[0].get_text()
        string_title = re.sub('\s+',' ',string_title) #se débarasse des \t et \n 
    except:
        string_title="\tRecipe title not found"
    return string_title

def getMarmiton(soup):

    html_ing = []
    html_qtt = []
    qtt = []
    ingredients = {}
    og_ing = []

    html_title = soup.findAll("h1",{"class":'main-title'}) 
    string_title = html_title[0].get_text()
    string_title = re.sub('\s+',' ',string_title) #se débarasse des \t et \n 

    html_ingredients_list = soup.find("div", {"class": "ingredient-list__ingredient-group"}) # select html tag with this class in recipe web page
    li_tags = html_ingredients_list.findAll("li") # object with all ingredients and quantities for the recipe

    
    for i in range(0,len(li_tags)):
        ing = [li_tags[i].find("div", {"class": "ingredient-data"}).get("data-singular"), li_tags[i].find("div", {"class": "ingredient-data"}).get("data-plural")]
        qty = li_tags[i].find("div", {"class": "quantity-data"}).get_text()
        unit = [li_tags[i].find("div", {"class": "unit-data"}).get("data-singular"), li_tags[i].find("div", {"class": "unit-data"}).get("data-plural")]
        val = [ing, qty, unit]
        ingredients[li_tags[i].find("div", {"class": "ingredient-data"}).get("data-singular")] = val
        # ing_line = html_ing[i].get("data-singular")
        # ingredients[ing_line]=html_qtt.get()
        # og_ing.append(ing_line)
        # ing = get_ing_only(ing_line)
    #     if ing[2] : 
    #         if qtt[i] == "" :
    #             qtt[i] =1
    #         if "/" not in str(qtt[i]):
    #             ingredients[ing[0]] = int(ing[1])*float(qtt[i])
    #         else: 
    #             ingredients[ing[0]] = ing[1]*0.5
    #     else :
    #         ingredients[ing[0]] = "Non ponderable"
    return ingredients

def get750g(soup):

    html_ing = []
    html_qtt = []
    qtt = []
    ingredients = {}
    og_ing = []

    print("recette 750g")
    html_ing = soup.findAll('span',{"class":'recipe-ingredients-item-label'})
    for i in range(0,len(html_ing)) :
        ing_line = html_ing[i].get_text()
        ing = get_ing_only(ing_line) 
        ingredients[ing[0]] = ing[1] 
    return ingredients

def getCuisineaz(soup):

    html_ing = []
    html_qtt = []
    qtt = []
    ingredients = {}
    og_ing = []

    print("recette cuisineaz")
    html_ing_whole = soup.findAll('ul',{"class":'txt-dark-gray'})
    html_ing = []
    # print(html_ing.split())
    # soup2 = BeautifulSoup(html_ing[0], 'html.parser')
    for line in html_ing_whole[0] :
        if line != '\n':
            html_ing.append(line)
    for i in range(0,len(html_ing)) :
        ing_line = html_ing[i].get_text()
        # print(res) 
        # print(ing_line)
        ing = get_ing_only(ing_line) 
        ingredients[ing[0]] = ing[1]
    return ingredients

if __name__ == "__main__":

    url = 'https://www.marmiton.org/recettes/recette_pizza-gaufree-au-fromage_347268.aspx'
    print(get_title(url))
    print(process("https://www.marmiton.org/recettes/recette_bruschetta-a-la-mozzarella_30276.aspx"))