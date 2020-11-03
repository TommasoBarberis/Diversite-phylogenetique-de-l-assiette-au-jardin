from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from get_NCBI_taxonomy import get_taxid
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Pré-requis : 
# pip install selenium
# pip install webdriver_manager



try :
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
except:
    driver = webdriver.Chrome(ChromeDriverManager().install())

# Création de la liste ID à partir de la liste espèce donnée
liste_espece = ['Homo sapiens', 'primate']
liste_ID = list(get_taxid(liste_espece))
# Ouverture du navigateur sur le site suivant
driver.get("http://lifemap-ncbi.univ-lyon1.fr/")
# Ajout des éléments dans la zone de texte
inputElement = driver.find_element_by_id("textarea")
inputElement.send_keys(str(liste_ID))
# Détéction du bouton View et click effectué
View = driver.find_element_by_id("viewMulti")
View.click()




