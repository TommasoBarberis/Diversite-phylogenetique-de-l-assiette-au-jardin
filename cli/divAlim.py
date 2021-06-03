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

if sys.argv[1]=="-f":
    pass
    # TODO multi recipe feature

elif sys.argv[1]=="-u":
    url = sys.argv[2]

    # Test if the recipe come from Marmiton
    domain = urlparse(url).netloc
    if domain != "www.marmiton.org":
        print("err: invalid domain, please take a recipe from marmiton.org")
        logger.error("{} has invalid domain".format(url))

    else:
        try:
            ingredients = get_ing.process(url)
            logger.info("Parsing {}".format(url))
        except Exception:
            print("err: impossible to parse {}".format(url))
            logger.exception("Error in parsing")
            sys.exit()

        if ingredients is None:
            print("err: impossible to parse {}".format(url))
            logger.exception("Error in parsing")
            sys.exit()
        else:
            #generate data
            name_recipe = get_ing.get_title(url)
            html_name = sys.argv[3] + "/" + name_recipe.replace(" ", "_") + ".html"


            species = ing_to_esp.recherche_globale(ingredients)
            
            species_not_found = ""
            for ing in ingredients:
                if ing not in species.keys():
                    species_not_found += ing + ", "
            if species_not_found.endswith(","):
                species_not_found = species_not_found[:-1]
            if species_not_found == "":
                species_not_found = "-"

            dict_nut = ing_properties.get_dict_nut(ingredients)
            drym = ing_properties.dry_matter_dict_update(ingredients, dict_nut)

            ing_properties.build_table(ingredients, species, dict_nut, drym, name_recipe.replace(" ", "_")) 
            
            tree = get_lifeMap_subTree.build_tree(species)
            pd = get_dp.phylogenetic_diversity(tree, species)           
            wpd = get_dp.weighted_phylogenetic_diversity(tree, species, drym)
            shannon = get_dp.shannon(species, drym)
            simpson = get_dp.simpson(species, drym)

            taxids = ""
            # for ing in species:
            id_list = get_lifeMap_subTree.get_taxid(species)
            for taxa_id in id_list:
                taxids += str(taxa_id) + ","
            if taxids.endswith(","):
                taxids = taxids[:-2]

            # create a html page to display results
            script_dir = sys.argv[4]

            with open(html_name, "w") as html_page:
                html_page.write("""
<html>
    <head>
        <meta charset="utf-8">
        <title>{}</title>
        <link rel="stylesheet" href="{}"> 
        <script type="text/javascript" src="{}"></script>
    </head>

    <body onload="onLoad()">
        <div class="title">
            <h1 id="page-title"> Diversité phylogénétique de l'assiette 
                <div class="top-buttons-div">
                    <button type="button" class="btn" id="gitlab_button">
                        <img src="diversite-phylogenetique-de-l-assiette-au-jardin/assets/gitlab.png" width="80%" height="80%">
                    </button>
                    <button type="button" class="btn" id="ucbl_button">
                        <img src="diversite-phylogenetique-de-l-assiette-au-jardin/assets/ucbl.png" width="80%" height="80%">
                    </button>
                    <button type="button" class="btn" id="marmiton_button">
                        <img src="diversite-phylogenetique-de-l-assiette-au-jardin/assets/marmiton.png" width="80%" height="80%">
                    </button>
                </div>
            </h1>
        </div>

        <div class="recipe-info">
            <p><b>Name of the recipe: </b>{}</p>
            <p><b>URL of the recipe: </b>{}</p>
            <p><b>Number of ingredients: </b>{}</p>
            <p><b>Number of specie found for the ingredients: </b>{}</p>
            <p><b>Ingredients that haven't match with a species: </b>{}</p>
            <img src="{}">
            <p><b>Phylogenetic diversity: </b>{}</p>
            <p><b>Weighted phylogenetic diversity: </b>{}</p>
            <p><b>Shannon's index: </b>{}</p>
            <p><b>Simpson's index: </b>{}</p>
            <iframe src="{}?lang=en&tid={}&zoom=false&markers=true&tree=true&searchbar=false&clickableMarkers=true" title="LifeMap frame from local file" width="80%" height="60%"></iframe>
        </div>
    </body>
</html>
                """.format(name_recipe, (script_dir + "/cli/css/style.css"), (script_dir + "/cli/js/script.js"), \
                    name_recipe, url, len(ingredients), len(species), species_not_found, \
                    (script_dir + "/assets/figures/"+ name_recipe.replace(" ", "_") + ".png"), pd, wpd, shannon, \
                    simpson, (script_dir + "/cli/lifemap-frame/lifemap.html"), taxids))


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
