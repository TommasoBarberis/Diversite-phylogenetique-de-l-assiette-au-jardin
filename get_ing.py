# import urllib3
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import sys

def cleanAndPonderate(ing_comp_input):
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
            
    for line in elem_list_end:
        if ingredient.endswith(line) :
            ingredient = ingredient[:len(line)]
    ing_comp_output[0] = ingredient
    return ing_comp_output

#base units : g /  ml 
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

    #comment gérer les qttés des doublons ?
        
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
    string_title = html_title[0].get_text()
    string_title = re.sub('\s+',' ',string_title) #se débarasse des \t et \n 
    return string_title

def getMarmiton(soup):

    html_ing = []
    html_qtt = []
    qtt = []
    ingredients = {}
    og_ing = []

    html_title = soup.findAll("h1",{"class":'main-title'}) 
    html_ing = soup.findAll('span',{"class":'ingredient'})
    html_qtt = soup.findAll('span',{"class":'recipe-ingredient-qt'}) 
    # html_nb_unit = soup.findAll("span",{"class":'recipe-ingredients__qt-counter__value_container'}) #YOYOYOY Chopper le nombre d'unités(modifier les qtt)
    # real_qtt = soup.findAll("data-base-qt") #chopper data-base-qt ? (pb avec 1/2)
    # print(real_qtt)
    # print(html_ing)
    # print(html_nb_unit)
    string_title = html_title[0].get_text()
    string_title = re.sub('\s+',' ',string_title) #se débarasse des \t et \n 
    #print(string_title[1:])
    qtt = [d.text for d in html_qtt]
    # print(qtt)
    for i in range(0,len(html_ing)) :
        ing_line = html_ing[i].get_text()
        # print(ing_line)
        og_ing.append(ing_line)
        ing = get_ing_only(ing_line)
        if qtt[i] != "" : 
            if "/" not in qtt[i]:
                ingredients[ing[0]] = ing[1]*float(qtt[i])
            else: 
                ingredients[ing[0]] = ing[1]*0.5
        else :
            ingredients[ing[0]] = ing[1] #useless ?
    return ingredients

def get750(soup):

    html_ing = []
    html_qtt = []
    qtt = []
    ingredients = {}
    og_ing = []

    print("recette 750g")
    html_ing = soup.findAll('span',{"class":'recipe-ingredients-item-label'})
    # print(html_ing)
    for i in range(0,len(html_ing)) :
        ing_line = html_ing[i].get_text()
        ing = get_ing_only(ing_line) 
        ingredients[ing[0]] = ing[1] #qtt au début de ing_line
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