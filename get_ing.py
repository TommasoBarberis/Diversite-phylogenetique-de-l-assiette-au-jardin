# import urllib3
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
import sys


#tout convertire en matières sèches ?

#base units : g /  ml 
def get_ing_only (ing_line):
    
    comp =['',1]
    ing = ing_line.lower()

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

    #comment gérer les qttés des doublons ?
    for it in range (0,2) : #2 itérations de nettoyage
        if ing.startswith('l d\''):
            ing = ing[4:]
            comp[1] = comp[1]*1000
        elif ing.startswith('l de'):
            ing = ing[5:]
            comp[1] = comp[1]*1000
        elif ing.startswith('kg d\''):
            ing = ing[5:]
            comp[1] = comp[1]*1000
        elif ing.startswith('kg de'):
            ing = ing[6:]
            comp[1] = comp[1]*1000
        elif ing.startswith('mg d\''):
            ing = ing[5:]
            comp[1] =comp[1]*0.001
        elif ing.startswith('mg de'):
            ing = ing[6:]
            comp[1] =comp[1]*0.001
        elif ing.startswith('cl d\''):
            ing = ing[5:]
            comp[1] =comp[1]* 10
        elif ing.startswith('cl de'):
            ing = ing[6:]
            comp[1] =comp[1]* 10
    #Rassembler tout ce qui est à retirer dans un fichier ?
        elif ing.startswith('g d\''):
            ing = ing[4:]
        elif ing.startswith('g de') or ing.startswith("ml d\'") or ing.startswith("gros"):
            ing = ing[5:]
        elif ing.startswith('sauce') or ing.startswith('ml de '):
            ing = ing[6:]
        elif ing.startswith('pot de') or ing.startswith('jus de '):
            ing = ing[7:]
        elif ing.startswith('pâte de') or ing.startswith('pate de') or ing.startswith('huile d\'') or ing.startswith("brin de ") or ing.startswith('blanc d\'') or ing.startswith('jaune d\'') or ing.startswith('boîte d\'') :
            ing = ing[8:]
        elif ing.startswith('verre de') or ing.startswith('gousse d\'') or ing.startswith('poudre d\'') or ing.startswith('zeste de ') or ing.startswith('bâton de') or ing.startswith('blancs d\'') or ing.startswith('jaunes d\'') or ing.startswith('boite de') or ing.startswith('boîte de'):
            ing = ing[9:]
        elif ing.startswith('gousses d\'') or ing.startswith('verres de') or ing.startswith('sachet de') or ing.startswith('copeau de ') or ing.startswith('paquet de') or ing.startswith('pincée de ') or ing.startswith('gousse de '):
            ing = ing[10:]
        elif ing.startswith('feuille de') or ing.startswith('rouleau de ') or ing.startswith("branche de ") or ing.startswith('cuillère d\'') or ing.startswith('poignée de') or ing.startswith('gousses de ') or ing.startswith('copeaux de ') or ing.startswith("bouquet de") or ing.startswith("tranche de "):
            ing = ing[11:]
        elif ing.startswith('feuilles de') or ing.startswith("noisette de") or ing.startswith("tranches de ") or ing.startswith('marmelade d\'') or ing.startswith('cuillère de') or ing.startswith('cuillères d\'') or ing.startswith("bouquets de"):
            ing = ing[12:]
        elif ing.startswith('cuillères de') or ing.startswith("concentré de") or ing.startswith("noisette de") or ing.startswith("tranche de "):
            ing = ing[13:]
        elif ing.startswith('petit verre de'):
            ing = ing[15:]
        elif ing.startswith("petit morceau de "):
            ing = ing[17:]  
        elif ing.startswith('cuillère à café d\'') or ing.startswith('cuillère a café d\'') :
            ing = ing[18:]  
        elif ing.startswith('cuillère à soupe d\'') or ing.startswith("petits morceaux de ")  or ing.startswith('cuillère a soupe d\'') or ing.startswith('cuillère à café de ') or ing.startswith('cuillère a café de ') or ing.startswith('cuillères à café d\'') or ing.startswith('cuillères a café d\''):
            ing = ing[19:]
        elif ing.startswith('cuillères à soupe d\'') or ing.startswith('cuillères a soupe d\'') or ing.startswith('cuillères à café de ') or ing.startswith('cuillères a café de ') or ing.startswith('cuillère à soupe de ') or ing.startswith('cuillère a soupe de '):
            ing = ing[20:]
        elif ing.startswith('cuillères à soupe de') or ing.startswith('cuillères a soupe de') :
            ing = ing[21:]
    
    if ing.endswith('sec'):
        ing = ing[:-4]     
    if ing.endswith('rapé') or ing.endswith('râpé') or ing.endswith("amer") or ing.endswith("noir"):
        ing = ing[:-5]   
    elif ing.endswith('glace') or ing.endswith("frais"):
        ing = ing[:-6]  
    elif ing.endswith('nature'):
        ing = ing[:-7]  
    elif ing.endswith('épaisse') or ing.endswith("liquide"):
        ing = ing[:-8]   
    elif ing.endswith('fraîches'):
        ing = ing[:-9]         
    elif ing.endswith('en poudre') or ing.endswith('en grains') or ing.endswith('pâtissier'):
        ing = ing[:-10] 
    elif ing.endswith("demi-écrémé"):
        ing = ing[:-12]
    comp[0] = ing
    return comp

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
        print("Invalid domain")
        sys.exit(1)
    
    return ingredients

def getMarmiton(soup):

    html_ing = []
    html_qtt = []
    qtt = []
    ingredients = {}
    og_ing = []

    # print("recette marmiton")
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
    print(string_title[1:])
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
                ingredients[ing[0]] = ing[1] 
                pass
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
    print(process(url))