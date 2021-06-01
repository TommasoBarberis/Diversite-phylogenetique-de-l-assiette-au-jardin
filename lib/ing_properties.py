#  -*- coding: utf-8 -*-

import xlrd
import csv
from lib.ing_to_esp import similar
import logging

logger = logging.getLogger("ing_properties.py")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def open_book(file):
    book = xlrd.open_workbook(file)
    return book


def get_default_line_number(ingredient):
    """
    Permet de trouver plus facilement certains ingrédients dans la table Ciqual. 
    """
    f = open("data/default.txt", "r", encoding = "utf-8")
    default_list = f.read().splitlines()
    for line in default_list:
        if ingredient in line: 
            value = line.split("/")
            return int(value[1])-1
    return 0


def get_nut_info(ing, book):
    score_threshold = 0.9
    sheet = book.sheets()[0]
    cpt = get_default_line_number(ing.lower())
    found_in_book = False
    nut_info = []
    final_nut_info = []
    highest_score = 0
    best_match = []
    row = 0
    if ing.endswith("s"):
        ing = ing[:len(ing)-1]
    if cpt != 0:
        found_in_book = True
        row = cpt
    else:
        for cel in sheet.col(7):
            values = cel.value.split(",")
            score = similar(values[0],ing)
            if score > highest_score:
                if cpt != 0 and score >= score_threshold:
                    highest_score = score
                    best_match.append([values[0],cpt])
                    row = cpt 
                    found_in_book = True
            cpt += 1


    if found_in_book:
        for cel in sheet.row(row):
            nut_info.append(cel.value)

        # In "Table_Ciqual_2020_FR_2020_07_07.xls":
        # name of ingredient:  column 7 
        # water (%): column 13
        # proteins (%): column 14
        # glucides (%): column 16
        # lipides (%): column 17 
        # sucres (%):column 18

        final_nut_info.append(nut_info[7]) # name
        final_nut_info.append(nut_info[13]) # water
        final_nut_info.append(nut_info[16]) # glucides
        final_nut_info.append(nut_info[17]) # lipides
        final_nut_info.append(nut_info[14]) # protéines

    logger.debug("The ingredient {} match in the Ciqual's table with {}".format(ing, final_nut_info))
    return final_nut_info


def get_dict_nut(dict_ing):
    myBook = open_book("data/Table_Ciqual_2020_FR_2020_07_07.xls")
    output = {}
    for ing in dict_ing:
        ingredient = ing.capitalize()  
        nut_info = get_nut_info(ingredient, myBook)
        if nut_info != []:
            output[ingredient] = nut_info
        else:
            output[ingredient] = ["-", "-", "-", "-", "-"]
    return output


def dry_matter_dict_update(dict_ing, dict_nut):
    dry_matter_dict = {}
    unit_list = ["g", "kg", "l", "cl"] # ponderable unit measure
    for ing in dict_ing:

        # if: l'ingredient est dans le dictionnaire contenant les informations nutritives et que sa quantite est 
        # non nulle et que la quantite d'eau est non nulle c'est alors possible de calculer la quantite de 
        # matiere seche

        if ing.capitalize() in dict_nut and dict_ing[ing][1] != 0 and dict_nut[ing.capitalize()][1] != '-' \
        and dict_ing[ing][1] is not None:

            if "<" in dict_nut[ing.capitalize()][1]:
                wat = float(format_float(str(dict_nut[ing.capitalize()][1][2:])))
            else:
                wat = float(format_float(str(dict_nut[ing.capitalize()][1])))

            qtt = str(dict_ing[ing][1])
            unit = dict_ing[ing][2][0]

            if qtt != '' and unit in unit_list:
                
                qtt  = float(qtt)

                if unit == "g":
                    pass
                elif unit == "kg" or unit == "l":
                    qtt *= 1000
                elif unit == "cl":
                    qtt *= 10

                dry_matter = round(qtt - qtt * wat/100,2)
                dry_matter_dict[ing] = [dry_matter, "g"]
            else:
                with open("filtering/unit_mass.txt", "r") as f:
                    lines = f.readlines() # file that allow to get mass for some unit
        
                    for line in lines:
                        line = line.split("/")
                        if unit == line[0]:
                            qtt = float(line[1]) * float(qtt)
                            dry_matter = round(qtt - qtt * wat/100,2)
                            dry_matter_dict[ing] = [dry_matter, "g"]
                        else:
                            dry_matter_dict[ing] = "-"     
        else: 
            dry_matter_dict[ing] = "-"

    return dry_matter_dict


def format_float(input_string):
    """
    Permet d'extrapoler le pourcentage d'eau d'un ingredient
    """
    if "-" in input_string or "traces" in input_string:
        return 0
    else:
        return input_string.replace("< ", "").replace(",", ".")


def nut_printer(nut_dict):
    print('{:10.20}'.format("Database name"), '{:10.15}'.format("Water (%)"),'{:10.15}'.format("Glucides (%)"), \
        '{:10.15}'.format("Lipides (%)"), '{:10.15}'.format("Proteins (%)"), sep="\t \t")
    for names in nut_dict:
        if nut_dict[names] != []:
            for element in nut_dict[names]:
                print('{:10.15}'.format(element), end= "\t \t")
            print("")


def write_tsv(file_name, recipes_dict):
    list_column = ["Recette", "Ingrédient", "Espèce", "Quantité ", "Matière sèche (g)", "Eau (%)", "Glucides (%)", \
        "Lipides (%)", "Protéines (%)", "Diversité phylogénétique", "Diversité phylogénétique pondérée", \
        "Indice de Shannon", "Indice de Simpson", "URL de la recette"]

    with open(file_name, 'w', newline='') as tsvfile:
        # Header
        for element in list_column:
            tsvfile.write(element)
            tsvfile.write("\t")
        tsvfile.write("\n")

        # Recipe scope
        for recipe in recipes_dict:
            name_recipe = recipes_dict[recipe][5]
            pd = recipes_dict[recipe][4][0]
            wpd = recipes_dict[recipe][4][1]
            shannon = recipes_dict[recipe][4][2]
            simpson = recipes_dict[recipe][4][3]
            url = recipe

            # Ingredients scope
            ingredients = recipes_dict[recipe][0]
            species = recipes_dict[recipe][1]
            dict_nut = recipes_dict[recipe][2]
            drym = recipes_dict[recipe][3]

            for ing in ingredients:
                sp = species[ing]
                qty = ingredients[ing][1] + " " + ingredients[ing][2][1]
                dry_qty = drym[ing]
                if isinstance(dry_qty, list):
                    dry_qty = str(dry_qty[0]) + " " + dry_qty[1]
                water = dict_nut[ing.capitalize()][1]
                sugars = dict_nut[ing.capitalize()][2]
                lipides =dict_nut[ing.capitalize()][3]
                proteins = dict_nut[ing.capitalize()][4]

                line = name_recipe + "\t" + ing + "\t" + sp + "\t" + str(qty) + "\t" + dry_qty + "\t" + str(water) \
                    + "\t" + str(sugars) + "\t" + str(lipides) + "\t" + str(proteins) + "\t" + str(pd) + "\t" \
                    + str(wpd) + "\t" + str(shannon) + "\t" + str(simpson) + "\t" + url

                tsvfile.write(line + "\n")


if __name__ == "__main__":

    dico = {'boule de pâte à pizza': 1.0, 'olive': 1.0, 'boule de mozzarella': 1.0, 'origan': 1.0, \
        'coulis de tomate': 300.0, 'jambon cru': 4.0, 'champignon de paris': 200.0, 'pâte à pizza': 1.0, \
            'boules de mozzarella': 2.0, 'coulis': 300.0, 'jambon': 4.0}
    dicnut = get_dict_nut(dico)
    drymatterdico = dry_matter_dict_update(dico,dicnut)
    # print(drymatterdico)

    filename = "data/Table_Ciqual_2020_FR_2020_07_07.xls"
    book = open_book(filename)
    print(type(book))
