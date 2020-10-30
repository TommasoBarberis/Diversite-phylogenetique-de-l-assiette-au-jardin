from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from get_NCBI_taxonomy import get_taxid


liste_espece = ['Homo sapiens', 'primate']
liste_ID = list(get_taxid(liste_espece))

Path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(Path)
driver.get("http://lifemap-ncbi.univ-lyon1.fr/")
inputElement = driver.find_element_by_id("textarea")
inputElement.send_keys(str(liste_ID))
View = driver.find_element_by_id("viewMulti")
View.click()




