# import urllib3
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re


#bas units : g /  ml 
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

    comp[0] = ing

    return comp

html_ing = []
html_qtt = []
qtt = []
ingredients = {}

url = 'https://www.750g.com/moules-a-la-creme-de-coco-et-a-la-citronnelle-r206858.htm'

req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

domain = urlparse(url).netloc

# print(domain) 

if domain == "www.marmiton.org" :
    print("recette marmiton")
    html_ing = soup.findAll('span',{"class":'ingredient'})
    html_qtt = soup.findAll('span',{"class":'recipe-ingredient-qt'})
    qtt = [d.text for d in html_qtt]
    for i in range(0,len(html_ing)) :
        ing_line = html_ing[i].get_text()
        ing = get_ing_only(ing_line)
        ingredients[ing[0]] = ing[1]*int(qtt[i])

elif domain == "www.750g.com" :
    print("recette 750g")
    html_ing = soup.findAll('span',{"class":'recipe-ingredients-item-label'})
    # print(html_ing)
    for i in range(0,len(html_ing)) :
        ing_line = html_ing[i].get_text()
        ing = get_ing_only(ing_line) 
        ingredients[ing[0]] = ing[1] #qtt au début de ing_line, trouver un moyen de la récup

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


elif domain == "www.cuisineactuelle.fr" :
    print("recette cuisineactuelle")

print(ingredients)
# print(qtt)

# print(ing)