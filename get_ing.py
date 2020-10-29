# import urllib3
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re


#tout convertire en matières sèches 

#base units : g /  ml 
def get_ing_only (ing_line):
    
    comp =['',1]
    ing = ing_line

    #remove space before number
    if ing.startswith(' ') :
        ing = ing_line[1:]
    
    #enlève la quantité si elle est présente au début de la ligne
    temp = re.findall(r'\d+', ing) 
    res = list(map(int, temp))
    if res != [] : 
        ing = ing[(len(str(res[0]))):]
        comp[1] = res[0]
        if ing.startswith(',') :
            ing = ing[(len(str(res[1]))+1):]
            comp[1] = comp[1] + res[1]*0.1
            

    #remove space after number
    if ing.startswith(' ') :
        ing = ing[1:]

    #prévoir 2 itérations ? (pour éviter ex: "cuillère de pate de" )
    if ing.startswith('g de'):
        ing = ing[5:]
    elif ing.startswith('l de'):
        ing = ing[5:]
        comp[1] = comp[1]*1000
    elif ing.startswith('kg de'):
        ing = ing[6:]
        comp[1] = comp[1]*1000
    elif ing.startswith('mg de'):
        ing = ing[6:]
        comp[1] =comp[1]*0.001
    elif ing.startswith('cl de'):
        ing = ing[6:]
        comp[1] =comp[1]* 10
    elif ing.startswith('pot de'):
        ing = ing[7:]
    elif ing.startswith('verre de'):
        ing = ing[9:]

    if ing.endswith('rapé') or ing.endswith('râpé'):
        ing = ing[:-5]   


    comp[0] = ing

    return comp

html_ing = []
html_qtt = []
qtt = []
ingredients = {}

url = 'https://www.marmiton.org/recettes/recette_poulet-thai-sauce-cacahuetes_12205.aspx'
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

domain = urlparse(url).netloc

# print(domain) 



# choper nom recette 
if domain == "www.marmiton.org" :
    print("recette marmiton")
    html_title = soup.findAll("h1",{"class":'main-title'}) #comment se débarasser des \t et \n ?
    html_ing = soup.findAll('span',{"class":'ingredient'})
    html_qtt = soup.findAll('span',{"class":'recipe-ingredient-qt'}) 
    # html_nb_unit = soup.findAll("span",{"class":'recipe-ingredients__qt-counter__value_container'}) #YOYOYOY Chopper le nombre d'unités(modifier les qtt)
    # real_qtt = soup.findAll("data-base-qt") #chopper data-base-qt ? (pb avec 1/2)
    # print(real_qtt)
    # print(html_ing)
    # print(html_nb_unit)
    string_title = html_title[0].get_text()
    string_title = re.sub('\s+',' ',string_title)
    print(string_title)
    qtt = [d.text for d in html_qtt]
    # print(qtt)
    for i in range(0,len(html_ing)) :
        ing_line = html_ing[i].get_text()
        # print(ing_line)
        ing = get_ing_only(ing_line)
        if qtt[i] != "" :
            if "/" not in qtt[i]:
                ingredients[ing[0]] = ing[1]*float(qtt[i])
            else: 
                print("soulaaaaant le slash")
                pass
        else :
            ingredients[ing[0]] = ing[1]

elif domain == "www.750g.com" :
    print("recette 750g")
    html_ing = soup.findAll('span',{"class":'recipe-ingredients-item-label'})
    # print(html_ing)
    for i in range(0,len(html_ing)) :
        ing_line = html_ing[i].get_text()
        ing = get_ing_only(ing_line) 
        ingredients[ing[0]] = ing[1] #qtt au début de ing_line

elif domain == "www.cuisineaz.com" :
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



print(ingredients)
# print(qtt)

# print(ing)