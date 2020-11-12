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

def get_subTree(especes):

    ''' fonction qui permait d'afficher le sous arbre sur le site web lifemap-ncbi.univ-lyon1.fr. '''

    # Création de la liste ID à partir de la liste espèce donnée
    liste_ID = (get_taxid(especes))
    liste_ID = str(liste_ID).strip('[]')
    # Ouverture du navigateur sur le site suivant
    driver = get_driver()
    driver.get("http://lifemap-ncbi.univ-lyon1.fr/")
    # Ajout des éléments dans la zone de texte
    inputElement = driver.find_element_by_id("textarea")
    inputElement.send_keys(str(liste_ID))
    # Détéction du bouton View et click effectué
    driver.find_element_by_id("viewMulti").click()
    driver.maximize_window()



def get_driver():

    ''' fonction qui permait de charger le bon driver web pour lancer soit firefox, soit chrome, soit Edge. '''

    # obtain directory for download
    directory_firefox = repr(os.path.dirname(os.path.realpath(sys.argv[0]))).strip("'")
    directory_chrome = repr(os.path.dirname(os.path.realpath(sys.argv[0])))

    # test pour connaitre quel navigateur est sur la machine
    try :
        firefox_options = webdriver.FirefoxProfile()
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                            "text/plain, text/html, text/css, text/javascript")
        firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_options.set_preference("browser.download.dir", directory_firefox)
        firefox_options.set_preference("browser.download.folderList", 2)

        driver = webdriver.Firefox(firefox_profile=firefox_options, executable_path=GeckoDriverManager().install())
    except :
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("prefs", {
            "download.default_directory": directory_chrome, 
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            })

            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
        except :
            driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    return driver


def get_newick(especes):

    ''' fonction qui permait de télécharger l'arbre phylogénétique sous format newick. 
    Le fichier newick sera téléchargé dans le repertoire où se trouve le script qui s'exécute '''

    driver = get_driver()
    driver.minimize_window()
    liste_ID = (get_taxid(especes))
    liste_ID = str(liste_ID).strip('[]')
    # Ouverture du navigateur sur le site suivant
    driver.get("https://phylot.biobyte.de/")
    # Ajout des éléments dans la zone de texte
    driver.find_element_by_id("treeElements").send_keys(str(liste_ID))
    driver.find_element_by_xpath("/html/body/div[@class='container']/div[@id='phylotContent']/div[@id='ncbi']/div[@id='mainForm']\
                                /div[@class='col']/form[@id='phylotForm']/div[@id='options']/div[@class='col'][2]/div[@class='row'][1]/div[@class='col-sm']\
                                    [2]/input[@class='form-control']").send_keys('Tree.txt')

    driver.find_element_by_xpath("/html/body/div[@class='container']/div[@id='phylotContent']/div[@id='ncbi']/div[@id='mainForm']/div[@class='col']\
                                /form[@id='phylotForm']/div[@id='options']/div[@class='col'][1]/div[@class='row'][1]/div[@class='col-sm'][3]/div[@class='radio']\
                                    [1]/label/input").send_keys(Keys.ARROW_DOWN)

    # Détéction du bouton generate tree file et Enter effectué
    driver.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.ENTER)
    # Wait 3 seconds for downloading
    time.sleep(3)
    driver.close()


