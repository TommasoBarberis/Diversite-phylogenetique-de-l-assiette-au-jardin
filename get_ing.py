# import urllib3
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

#bas units : g /  ml 
def get_ing_only (ing_line):
    
    comp =['',1]
    ing = ing_line

    if ing.startswith(' ') :
        ing = ing_line[1:]
    elif ing.startswith('g de'):
        ing = ing_line[5:]
    elif ing.startswith('l de'):
        ing = ing_line[5:]
        comp[1] = 1000
    elif ing.startswith('kg de'):
        ing = ing_line[6:]
        comp[1] = 1000
    elif ing.startswith('mg de'):
        ing = ing_line[6:]
        comp[1] = 0.001
    elif ing.startswith('cl de'):
        ing = ing_line[6:]
        comp[1] = 10

    comp[0] = ing

    return comp

html_ing = []
html_qtt = []
qtt = []

url = 'https://www.marmiton.org/recettes/recette_tarte-thon-et-tomate_14139.aspx'

req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

domain = urlparse(url).netloc

print(domain) 

if domain == "www.marmiton.org" :
    print("recette marmiton")
    html_ing = soup.findAll('span',{"class":'ingredient'})
    html_qtt = soup.findAll('span',{"class":'recipe-ingredient-qt'})
    qtt = [d.text for d in html_qtt]

for i in range(0,len(qtt)) :
    if qtt[i] == '' :
        qtt[i] = 1

ingredients = {}

for i in range(0,len(html_ing)) :
    ing_line = html_ing[i].get_text()
    
    ing = get_ing_only(ing_line)

    ingredients[ing[0]] = ing[1]*int(qtt[i])
# print(qtt)

print(ingredients)
# print(qtt)

# print(ing)