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
    f = open("data/default.txt", "r")
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
                            dry_matter = str(float(line[1]) * float(qtt))
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


def write_tsv(file_name,dico_ing, dico_especes, dry_matter_dico, dico_nut):
    ing_list = list(dico_ing.keys())
    list_column = ["Ingrédient", "Espèce", "Quantité ", "Matière sèche (g)", "Eau (%)", "Glucides (%)", "Lipides (%)", \
        "Protéines, N x facteur de Jones (%)"]
    with open(file_name, 'w', newline='') as tsvfile:
        for element in list_column:
            tsvfile.write(element)
            tsvfile.write("\t")
        tsvfile.write("\n")
        for ing in ing_list:
            tsvfile.write(ing) # first column - ingredient
            tsvfile.write("\t")
            ing_cap = ing.capitalize() 
            if ing in dico_especes:
                tsvfile.write(dico_especes[ing]) # second column -specie
            else:
                tsvfile.write("-") # second column - specie
            tsvfile.write("\t")
            tsvfile.write(str(dico_ing[ing][1] + " " + dico_ing[ing][2][1])) # third column - quantity
            tsvfile.write("\t")
            if ing in dry_matter_dico:
                if dry_matter_dico[ing] != "-":
                    tsvfile.write(str(dry_matter_dico[ing][0]) + " " + str(dry_matter_dico[ing][1])) # fourth column - dry matter quantity
                else:
                    tsvfile.write("-")
            else:
                tsvfile.write("-")
            tsvfile.write("\t")
            if ing_cap in dico_nut:
                for i in range(1, len(dico_nut[ing_cap])):
                    tsvfile.write(dico_nut[ing_cap][i])
                    tsvfile.write("\t")
            else:
                tsvfile.write("-\t-\t-\t-")
            tsvfile.write("\n")


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
