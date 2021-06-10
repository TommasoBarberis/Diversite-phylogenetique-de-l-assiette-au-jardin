#  -*- coding: utf-8 -*-
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from lib import get_lifeMap_subTree, get_ing, ing_to_esp, get_dp, ing_properties
import logging
from urllib.parse import urlparse

logger = logging.getLogger("divAlim.py")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# key: url of recipe
# value: list with ingredients, species, dictionary nutrition, dry matter dictionnary, phylogenetic diversity, 
# weighted phylogenetic diversity, shannon, simpson, list of taxaid
recipes_dict = {} 

if sys.argv[1] == "-f":
    file_name = sys.argv[2]

    with open(sys.argv[2], "r", encoding="utf-8") as f:
        list_url = f.readlines()
        for url in list_url:
            recipes_dict[url.replace("\n", "")] = []
    
    if "." in file_name:
        file_name = file_name[:file_name.rfind(".")]
    if "/" in file_name:
        file_name = file_name[file_name.rfind("/"):]


elif sys.argv[1] == "-u":
    url = sys.argv[2]
    file_name = get_ing.get_title(url)
    recipes_dict[url] = []

elif sys.argv[1] == "-t":
    file_name = sys.argv[2]

    with open(sys.argv[2], "r", encoding="utf-8") as f:
        lines = f.readlines()[1:] # skip the header
        n_fields = len(lines[0].split("\t"))
        if n_fields == 5:
            prev_key = lines[0].split("\t")[4].replace("\n", "")
        elif n_fields == 4:
            prev_key = lines[0].split("\t")[0]

        ingredients = {}
        for line in lines:
            fields = line.split("\t")
            name_recipe = fields[0]
            ing = fields[1]
            qty = fields[2]
            unit = fields[3]
            url = fields[4].replace("\n", "")
            val =[[ing, ing], qty, [unit, unit]]

            if n_fields == 5:
                key = url
            elif n_fields == 4:
                key = name_recipe

            if key != prev_key:
                recipes_dict[prev_key] = [ingredients]
                ingredients = {}
            else:
                ingredients[ing] = val
            prev_key = key

        recipes_dict[prev_key] = ingredients

    if "." in file_name:
        file_name = file_name[:file_name.rfind(".")]
    if "/" in file_name:
        file_name = file_name[file_name.rfind("/"):]


ingredients = None
counter = 1
file_name = file_name.replace(" ", "_")
try:
    os.makedirs(sys.argv[3] + "/" + file_name)
except:
    print("err: a report for this file/URL already exists")
    sys.exit()
os.makedirs(sys.argv[3] + "/" + file_name + "/assets")

html_name = sys.argv[3] + "/" + file_name + "/" + file_name + ".html"


for url in recipes_dict:
    if recipes_dict[url] != []:
        try:
            ingredients = recipes_dict[url]
        except:
            pass

        recipes_dict[url] = []
    else:
        try:
            logger.info("Parsing {}".format(url))
            ingredients = get_ing.process(url)
        except Exception:
            if sys.argv[1] == "-u":
                print("err: incorrect url: {}".format(url))
            if sys.argv[1] == "-f":
                print("err: incorrect url at the line: {}".format(counter))
            logger.exception("Invalid url")
            sys.exit()
        
        counter += 1

    try:
        assert ingredients is not None
    except Exception as err:
        print("err: impossible to parse {}".format(url))
        logger.exception(err)
        logger.error("Parse error")
        sys.exit()
    
    #generate data
    species = ing_to_esp.recherche_globale(ingredients)
    
    dict_nut = ing_properties.get_dict_nut(ingredients)
    drym = ing_properties.dry_matter_dict_update(ingredients, dict_nut)

    name_recipe = get_ing.get_title(url)
    if name_recipe == "\tRecipe title not found":
        name_recipe = url
    ing_properties.build_table(ingredients, species, dict_nut, drym, name_recipe.replace(" ", "_")) 

    tree = get_lifeMap_subTree.build_tree(species)
    pd = get_dp.phylogenetic_diversity(tree, species)     
    dict_sp_drym = {}
    bool_var = True
    for ing in species.keys():
        if species[ing] != "NA":
            if ing in drym.keys() and drym[ing] != "NA":
                dict_sp_drym[species[ing]] = drym[ing]
            else:
                bool_var = False
                break
    
    if bool_var:
        wpd = get_dp.weighted_phylogenetic_diversity(tree, species, dict_sp_drym)
        shannon = get_dp.shannon(species, dict_sp_drym)
        simpson = get_dp.simpson(species, dict_sp_drym)
    else:
        wpd = "NA"
        shannon = "NA"
        simpson = "NA"

    taxids = ""
    # for ing in species:
    id_list = get_lifeMap_subTree.get_taxid(species)
    for taxa_id in id_list:
        taxids += str(taxa_id) + ","
    if taxids.endswith(","):
        taxids = taxids[:-1]

    recipes_dict[url] = [name_recipe, ingredients, species, dict_nut, drym, pd, wpd, shannon, simpson, taxids]
    logger.info("URL processed, getting ingredient, species, nutrition data and dry matter information")


# create a html page to display results
script_dir = sys.argv[4]

with open(html_name, "w") as html_page:
    html_page.write(f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>{html_name.replace("_", " ")}</title>
            <link rel="stylesheet" href="{script_dir}/cli/css/style.css"> 
            <script type="text/javascript" src="{script_dir}/cli/js/script.js"></script>
        </head>

        <body onload="onLoad()">
            <div class="title">
                <h1 id="page-title"> Diversité phylogénétique de l'assiette 
                    <div class="top-buttons-div">
                        <button type="button" class="btn" id="gitlab_button">
                            <img src="{script_dir}/assets/gitlab.png" width="80%" height="80%">
                        </button>
                        <button type="button" class="btn" id="ucbl_button">
                            <img src="{script_dir}/assets/ucbl.png" width="80%" height="80%">
                        </button>
                        <button type="button" class="btn" id="marmiton_button">
                            <img src="{script_dir}/assets/marmiton.png" width="80%" height="80%">
                        </button>
                    </div>
                </h1>
            </div>
    """)


    for url in recipes_dict:
        species_not_found = ""
        for ing in recipes_dict[url][1]:
            if ing not in recipes_dict[url][2].keys():
                species_not_found += ing + ", "
        if species_not_found.endswith(",") or species_not_found.endswith(", "):
            index = species_not_found.rfind(",")
            species_not_found = species_not_found[:index]
        if species_not_found == "":
            species_not_found = "-"

        name_recipe = get_ing.get_title(url)
        if name_recipe == "\tRecipe title not found":   
            name_recipe = url
        os.rename(script_dir + "/assets/figures/"+ name_recipe.replace(" ", "_") + ".png", sys.argv[3] + "/" + file_name + "/assets/" + name_recipe.replace(" ", "_") + ".png")

        html_page.write(f"""
            <div id={recipes_dict[url][0].replace(" ", "-")} class="recipe-info">
                <p><b>Name of the recipe: </b>{recipes_dict[url][0]}</p>
                <p><b>URL of the recipe: </b>{url}</p>
                <p><b>Number of ingredients: </b>{len(recipes_dict[url][1])}</p>
                <p><b>Number of specie found for the ingredients: </b>{len(recipes_dict[url][2])}</p>
                <p><b>Ingredients that haven't match with a species: </b>{species_not_found}</p>
                <img src="{"assets/" + name_recipe.replace(" ", "_") + ".png"}">
                <p><b>Phylogenetic diversity: </b>{recipes_dict[url][5]}</p>
                <p><b>Weighted phylogenetic diversity: </b>{recipes_dict[url][6]}</p>
                <p><b>Shannon's index: </b>{recipes_dict[url][7]}</p>
                <p><b>Simpson's index: </b>{recipes_dict[url][8]}</p>
                <iframe src="{script_dir}/cli/lifemap-frame/lifemap.html?lang=en&tid={recipes_dict[url][9]}&zoom=false&markers=true&tree=true&searchbar=false&clickableMarkers=true&zoomButton=true&colorLine=2a9d8f&opacityLine=0.8&weightLine=6" title="LifeMap frame from local file" width="80%" height="60%"></iframe>
            </div>
        """)
    
    html_page.write(""" 
        </body>
    </html>
""")


# keep only last 1000 lines of the log file
try:
    with open("log.txt", "r") as log:
        lines = log.readlines()
        log_length = len(lines)
        if log_length > 1000:
            lines = lines[(log_length-1001):-1]

    with open("log.txt", "w") as log:
        for line in lines:
            log.write(line)
finally:
    pass