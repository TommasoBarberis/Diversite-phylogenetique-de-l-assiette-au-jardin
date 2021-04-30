# -- coding: utf-8 --

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from ete3 import Tree, TreeStyle,  NCBITaxa
import os, sys, time
import itertools
import logging

logger = logging.getLogger("get_lifeMap_subTree.py")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

os.environ['WDM_LOG_LEVEL'] = '0'
# Pré-requis : 
# pip install ete3
# pip install selenium
# pip install webdriver_manager


ncbi = NCBITaxa()

def get_taxid(liste_espece):
    liste_espece = liste_espece.values()
    if not isinstance(liste_espece, list):
        liste_espece=list(liste_espece)
    # Obtention des valeurs du dictionnaire
    Liste = [(ncbi.get_name_translator(liste_espece).values())]
    # Obtention d'une liste des valeurs du dictionnaire
    liste_nettoyée = list(itertools.chain(*[ss_elt for elt in Liste for ss_elt in zip(*elt)]))
    return liste_nettoyée


def get_subTree(especes):
    '''
     fonction qui permet d'afficher le sous arbre sur le site web lifemap-ncbi.univ-lyon1.fr.
    '''

    # Création de la liste ID à partir de la liste espèce donnée
    liste_ID = get_taxid(especes)
    liste_ID = str(liste_ID).strip('[]')

    # Ouverture du navigateur sur le site suivant
    driver = get_driver()
    driver.get("http://lifemap-ncbi.univ-lyon1.fr/")
    logger.info("Opening http://lifemap-ncbi.univ-lyon1.fr/")
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
    try:        
        try:
            firefox_options = webdriver.FirefoxProfile()
            firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                "text/plain, text/html, text/css, text/javascript")
            firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
            firefox_options.set_preference("browser.download.dir", directory_firefox)
            firefox_options.set_preference("browser.download.folderList", 2)

            driver = webdriver.Firefox(firefox_profile=firefox_options, executable_path=GeckoDriverManager().install())
            logger.info("Opening Firefox")
            return driver
        
        except Exception():
            logger.exception("Firefox driver doesn't work")

        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("prefs", {
            "download.default_directory": directory_chrome, 
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            })

            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
            logger.info("Opening Chrome")
            return driver
        
        except Exception:
            logger.exception("Chrome driver doesn't work")
        
        try:
            driver = webdriver.Edge(EdgeChromiumDriverManager().install())
            logger.info("Opening Edge")
            return driver
        except Exception:
            logger.exception("Edge driver doesn't work")
    except:
        logger.error("No driver found")


def get_newick(especes):
    ''' 
    Fonction qui permet de télécharger l'arbre phylogénétique sous format newick. 
    Le fichier newick sera téléchargé dans le repertoire où se trouve le script qui s'exécute.
    '''
    try:
        os.remove("Tree.txt")
    except:
        pass
    driver = get_driver()
    liste_ID = get_taxid(especes)
    liste_ID = str(liste_ID).strip('[]')

    # Ouverture du navigateur sur le site suivant
    driver.get("http://lifemap-ncbi.univ-lyon1.fr/#")

    # Ajout des éléments dans la zone de texte
    driver.find_element_by_id("textarea").send_keys(str(liste_ID))
    driver.find_element_by_id("getSubtree").click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, \
        "/html/body[@class='modal-open']/div[@id='ModalTreeFormat']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-body row whitish']/div[@class='col-sm-4'][2]/div[@class='radio'][2]/label/input"\
            ))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, \
        "/html/body[@class='modal-open']/div[@id='ModalTreeFormat']/div[@class='modal-dialog']/div[@class='modal-content']/div[@class='modal-body row whitish']/div[@class='col-sm-4'][3]/div[@class='radio'][2]/label/input"\
            ))).click()
            
    # time.sleep(5)
    # driver.minimize_window()
    with open("Tree.txt","w") as tree:
        tree.write(str(driver.find_element_by_xpath('//*[@id="TreeTextarea"]').get_attribute("value")))
    driver.find_element_by_xpath('//*[@id="ModalTreeFormat"]/div/div/div[4]/div/div[2]/button').click()
    # driver.close()


def subtree_from_newick():
    # get_newick(especes)
    t = Tree('Tree.txt', quoted_node_names = True, format = 1)   
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.branch_vertical_margin = 10 # 10 pixels between adjacent branches
    t.show(tree_style = ts)


if  __name__ == "__main__":
    species = {"vache": "Bos taurus", "poulet":"Gallus gallus", "homme": "Homo sapiens"}
    # get_subTree(species)
    subtree_from_newick()