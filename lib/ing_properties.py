#  -*- coding: utf-8 -*-

import xlrd
import csv
from lib.ing_to_esp import similar
import plotly.graph_objects as go
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
        # calories (kJ): column 9
        # water (%): column 13
        # proteins (%): column 14
        # glucides (%): column 16
        # lipides (%): column 17 
        # sucres (%):column 18

        final_nut_info.append(nut_info[7]) # name
        final_nut_info.append("NA" if (nut_info[9] == "-" or nut_info[9] == "traces") else nut_info[9].replace("<", "")) # calories
        final_nut_info.append("NA" if (nut_info[13] == "-" or nut_info[13] == "traces") else nut_info[13].replace("<", "")) # water
        final_nut_info.append("NA" if (nut_info[16] == "-" or nut_info[16] == "traces") else nut_info[16].replace("<", "")) # glucides
        final_nut_info.append("NA" if (nut_info[17] == "-" or nut_info[17] == "traces") else nut_info[17].replace("<", "")) # lipides
        final_nut_info.append("NA" if (nut_info[14] == "-" or nut_info[14] == "traces") else nut_info[14].replace("<", "")) # protéines

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
            output[ingredient] = ["NA", "NA", "NA", "NA", "NA", "NA"]
    return output


def convert_to_g(qty, unit):
    try:
        qty  = float(qty)
    except:
        return "NA"

    if unit == "g" or unit == "ml":
        pass
    elif unit == "kg" or unit == "l":
        qty *= 1000
    elif unit == "cl":
        qty *= 10
    elif unit == "dl":
        qty *= 100
    
    return qty


def dry_matter_dict_update(dict_ing, dict_nut):
    dry_matter_dict = {}
    unit_list = ["g", "kg", "l", "dl", "cl", "ml"] # ponderable unit measure
    for ing in dict_ing:

        # if: l'ingredient est dans le dictionnaire contenant les informations nutritives et que sa quantite est 
        # non nulle et que la quantite d'eau est non nulle c'est alors possible de calculer la quantite de 
        # matiere seche

        if ing.capitalize() in dict_nut and dict_ing[ing][1] != 0 and dict_nut[ing.capitalize()][2] != 'NA' \
        and dict_ing[ing][1] is not None:            

            if "<" in dict_nut[ing.capitalize()][1]:
                wat = float(format_float(str(dict_nut[ing.capitalize()][2][2:])))
            else:
                wat = float(format_float(str(dict_nut[ing.capitalize()][2])))

            qtt = str(dict_ing[ing][1])
            unit = dict_ing[ing][2][0]

            if qtt != '' and unit in unit_list:
                
                qtt = convert_to_g(qtt, unit)
                dry_matter = round(qtt - (qtt * (wat / 100)), 2)
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
                            dry_matter_dict[ing] = "NA"     
        else: 
            dry_matter_dict[ing] = "NA"

    return dry_matter_dict


def format_float(input_string):
    """
    Permet d'extrapoler le pourcentage d'eau d'un ingredient
    """
    if "NA" in input_string or "traces" in input_string:
        return 0
    else:
        return input_string.replace("< ", "").replace(",", ".")


def write_tsv(file_name, recipes_dict):
    list_column = ["Recipe", "Ingredient", "Specie", "Quantity", "Dry_matter", "Energy", "Water", "Glucides", \
        "Lipids", "Proteins", "Richness", "Phylogenetic_diversity", "Weighted_phylogenetic_diversity", \
        "Shannon", "Simpson", "URL"]

    with open(file_name, 'w', newline='') as tsvfile:
        # Header
        header_line = ""
        for element in list_column:
            header_line += element + "\t"
        if header_line.endswith("\t"):
            header_line = header_line[:-1]
        tsvfile.write(header_line + "\n")


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
            richness = len(set(species.values()))
            if "NA" in species.values():
                richness -= 1            

            for ing in ingredients:
                if ing != "":
                    try:
                        sp = species[ing]
                    except:
                        sp = "NA"

                    qty = ingredients[ing][1] + " " + ingredients[ing][2][1]
                    dry_qty = drym[ing]
                    if isinstance(dry_qty, list):
                        dry_qty = str(dry_qty[0]) + " " + dry_qty[1]
                    try:
                        cal = float(dict_nut[ing.capitalize()][1].replace(",", ".")) # * float(convert_to_g(ingredients[ing][1], ingredients[ing][2][0]))) / 100
                    except:
                        cal = "NA"
                    water = dict_nut[ing.capitalize()][2].replace(",", ".")
                    sugars = dict_nut[ing.capitalize()][3].replace(",", ".")
                    lipides =dict_nut[ing.capitalize()][4].replace(",", ".")
                    proteins = dict_nut[ing.capitalize()][5].replace(",", ".")

                    line = name_recipe + "\t" + ing + "\t" + sp + "\t" + str(qty) + "\t" + dry_qty + "\t" + str(cal) \
                        + "\t" + str(water) + "\t" + str(sugars) + "\t" + str(lipides) + "\t" + str(proteins) \
                        + "\t" + str(richness) + "\t" + str(pd) + "\t" + str(wpd) + "\t" + str(shannon) \
                        + "\t" + str(simpson) + "\t" + url

                    tsvfile.write(line + "\n")
        tsvfile.write("\n")


def build_table(ingredients, species, dict_nut, drym, recipe_title):
    sp = []
    quantities = []
    drym_quantities = []
    cal = []
    water = []
    sugars = []
    lipides = []
    proteins = []

    for ing in ingredients:
        if ing in species.keys():
            sp.append(species[ing])
        else:
            sp.append("NA")

        qty = ingredients[ing][1] + " " + ingredients[ing][2][0]
        if qty == " ":
            quantities.append("NA")
        else:
            quantities.append(qty)

        if ing in drym.keys():
            if drym[ing] == "NA":
                drym_quantities.append(drym[ing])
            else:
                drym_quantities.append(str(drym[ing][0]) + " " + drym[ing][1])

        if ing.capitalize() in dict_nut.keys():
            try:
                qtt = convert_to_g(ingredients[ing][1], ingredients[ing][2][0])
                cal_val = float(dict_nut[ing.capitalize()][1]) #* float(qtt)) / 100
            except:
                cal_val = "NA"
                    
            cal.append(cal_val)
            water.append(dict_nut[ing.capitalize()][2])
            sugars.append(dict_nut[ing.capitalize()][3])
            lipides.append(dict_nut[ing.capitalize()][4])
            proteins.append(dict_nut[ing.capitalize()][5])
        else:
            water.append("NA")
            sugars.append("NA")
            lipides.append("NA")
            proteins.append("NA")
            
    species = sp
    ingredients = list(ingredients.keys())

    table = go.Figure(data = [go.Table(header = dict(values = ["Ingrédient", "Espèce", "Quantité", \
        "Qté de matière\n sèche (g)", "Énergie (kJ)", "Eau (%)", "Glucides (%)", "Lipides (%)", "Protéines (%)"], font_size = 18, height = 60), \
        cells = dict(values = [ingredients, species, quantities, drym_quantities, cal, water, sugars, lipides, proteins], \
        font_size = 16, height = 50))], layout = go.Layout(paper_bgcolor = "rgba(0,0,0,0)", height = ((60 * len(ingredients)) + 60), width = 1200, margin = dict(b = 0, t = 0, l = 0, r = 0))) # 


    table.write_image("assets/figures/" + recipe_title + ".png")
    return None



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
