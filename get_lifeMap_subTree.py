# -- coding: utf-8 --
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from get_NCBI_taxonomy import get_taxid
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from ete3 import Tree, PhyloTree
import os, sys, time



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
liste_espece = ['Saccharum officinarum', 'Gallus gallus domesticus', 'Rhodocera rhamni', 'Pistacia vera']
liste_ID = (get_taxid(liste_espece))
liste_ID = str(liste_ID).strip('[]')
# Ouverture du navigateur sur le site suivant
driver.get("http://lifemap-ncbi.univ-lyon1.fr/")
# Ajout des éléments dans la zone de texte
inputElement = driver.find_element_by_id("textarea")
inputElement.send_keys(str(liste_ID))
# Détéction du bouton View et click effectué
View = driver.find_element_by_id("viewMulti").click()

# obtain directory for download

directory = repr(os.path.dirname(os.path.realpath(sys.argv[0]))).strip("'")

# test pour connaitre quel navigateur est sur la machine
try :
    firefox_options = webdriver.FirefoxProfile()
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "text/plain, text/html, text/css, text/javascript")
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_options.set_preference("browser.download.dir", directory)
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("pdfjs.disabled", True)

    driver2 = webdriver.Firefox(firefox_profile=firefox_options, executable_path=GeckoDriverManager().install())
except :
    try:
        driver2 = webdriver.Chrome(ChromeDriverManager().install())
    except :
        driver2 = webdriver.Edge(EdgeChromiumDriverManager().install())
driver2.minimize_window()
driver.maximize_window()
# Ouverture du navigateur sur le site suivant
driver2.get("https://phylot.biobyte.de/")
# Ajout des éléments dans la zone de texte
inputElement = driver2.find_element_by_id("treeElements")
inputElement.send_keys(str(liste_ID))
driver2.find_element_by_xpath("/html/body/div[@class='container']/div[@id='phylotContent']/div[@id='ncbi']/div[@id='mainForm']\
                            /div[@class='col']/form[@id='phylotForm']/div[@id='options']/div[@class='col'][2]/div[@class='row'][1]/div[@class='col-sm']\
                                [2]/input[@class='form-control']").send_keys('Tree.txt')

driver2.find_element_by_xpath("/html/body/div[@class='container']/div[@id='phylotContent']/div[@id='ncbi']/div[@id='mainForm']\
                        /div[@class='col']/form[@id='phylotForm']/div[@id='options']/div[@class='col'][1]/div[@class='row'][1]/div[@class='col-sm']\
                            [3]/div[@class='radio'][2]/label/input").send_keys(Keys.ENTER)

# Détéction du bouton generate tree file et Enter effectué
driver2.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.ENTER)
time.sleep(3)
driver2.close()

# Load a tree structure from a newick file.


