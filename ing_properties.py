import xlrd

# name : 7 
# water % : 13
# glucides % 16
# lipides % 17 
# sucres % 18

def openBook(file):
    book = xlrd.open_workbook(file)
    return book

def getNutInfo(ing,book):
    sheet = book.sheets()[0]
    cpt = 0
    found_in_book = False
    # ing = "Pomme de terre"
    nut_info = []
    final_nut_info = []
    for cel in sheet.col(7):
        if (cel.value.startswith(ing) or cel.value.startswith(ing[:-1])) and "crue" in cel.value:
            # print(cel.value)
            found_in_book = True
            break
        cpt +=1
    
    if not found_in_book :
        cpt = 0
        for cel in sheet.col(7):
            if (cel.value.startswith(ing) or cel.value.startswith(ing[:-1])):
                # print(cel.value)
                found_in_book = True
                break
            cpt +=1

    if found_in_book : 
        for cel in sheet.row(cpt) :
            nut_info.append(cel.value)

        final_nut_info.append(nut_info[7])
        final_nut_info.append(nut_info[13])
        final_nut_info.append(nut_info[16])
        final_nut_info.append(nut_info[17])
        final_nut_info.append(nut_info[18])
    return final_nut_info

#{"ingredient" : [dry_matter,glucide,lipides,sucres]}
def getDictNut(ing_dict):
    myBook = openBook("nutrition_db/Table_Ciqual_2020_FR_2020_07_07.xls")
    output={}
    for ing in ing_dict :
        ingredient = ing.capitalize()
        output[ingredient] = getNutInfo(ingredient,myBook)
    return output

if __name__ == "__main__":

    dico = {'boule de pâte à pizza': 1.0, 'olive': 1.0, 'boule de mozzarella': 1.0, 'origan': 1.0, 'coulis de tomate': 300.0, 'jambon cru': 4.0, 'champignon de paris': 200.0, 'pâte à pizza': 1.0, 'boules de mozzarella': 2.0, 'coulis': 300.0, 'jambon': 4.0}
    getDictNut(dico)
    output = getDictNut(dico)
    print(output)
    # print(getNutInfo("Tomate",myBook))