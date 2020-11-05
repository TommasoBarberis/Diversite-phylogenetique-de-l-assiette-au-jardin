from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from get_NCBI_taxonomy import get_taxid
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Pré-requis : 
# pip install ete3
# pip install selenium
# pip install webdriver_manager

# test pour connaitre quel navigateur est sur la machine
try :
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
except :
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    except :
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())


# Création de la liste ID à partir de la liste espèce donnée
liste_espece = ['Homo sapiens', 'primate']
liste_ID = (get_taxid(liste_espece))
liste_ID = str(liste_ID).strip('[]')
# Ouverture du navigateur sur le site suivant
driver.get("http://lifemap-ncbi.univ-lyon1.fr/")
# Ajout des éléments dans la zone de texte
inputElement = driver.find_element_by_id("textarea")
inputElement.send_keys(str(liste_ID))
# Détéction du bouton View et click effectué
View = driver.find_element_by_id("viewMulti").click()

# obtain newick tree

# test pour connaitre quel navigateur est sur la machine
try :
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
except :
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    except :
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

# Ouverture du navigateur sur le site suivant
driver.get("https://phylot.biobyte.de/")
# Ajout des éléments dans la zone de texte
inputElement = driver.find_element_by_id("treeElements")
inputElement.send_keys(str(liste_ID))
# Détéction du bouton View et click effectué
View = driver.find_element_by_xpath("//input[@type='submit']").click()
