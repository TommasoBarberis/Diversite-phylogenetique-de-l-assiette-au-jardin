import xlrd

# name : 7 
# water % : 13
# glucides % 16
# lipides % 17 
# sucres % 18

#faire une classe ingrédient ?

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
        if ing.endswith("s"):
            if (cel.value.startswith(ing) or cel.value.startswith(ing[:-1])) and ("crue" in cel.value or "cru" in cel.value):
                found_in_book = True
                break
        else :
            if (cel.value.startswith(ing)) and ("crue" in cel.value or "cru" in cel.value):
                found_in_book = True
                break
        cpt +=1
    
    if not found_in_book :
        cpt = 0
        if ing.endswith("s"):
            for cel in sheet.col(7):
                if (cel.value.startswith(ing) or cel.value.startswith(ing[:-1])):
                    found_in_book = True
                    break
                cpt +=1
        else : 
            for cel in sheet.col(7):
                if (cel.value.startswith(ing)):
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

#{"ingredient" : [db_name,water_qtt,glucide,lipides,sucres]}
def getDictNut(dict_ing):
    myBook = openBook("nutrition_db/Table_Ciqual_2020_FR_2020_07_07.xls")
    output={}
    for ing in dict_ing :
        ingredient = ing.capitalize()  
        nut_info =  getNutInfo(ingredient,myBook)
        if nut_info != []:
            output[ingredient] = nut_info
    return output

def getDictNutPond(dict_ing, dict_nut):
    dict_pond = {}
    for ing in dict_nut :
        dict_pond[ing] = []
        dict_pond[ing].append(dict_nut[ing][0])

        qtt = dict_ing[ing.lower()]
        print(qtt)
        wat_pond = int(qtt) * int(dict_nut[ing][1])/100 
        gluc_pond = int(qtt) * int(dict_nut[ing][2])/100
        lip_pond = int(qtt) * int(dict_nut[ing][3])/100
        suc_pond = int(qtt) * int(dict_nut[ing][4])/100

        



def nutPrinter(nut_dict):
    print('{:10.20}'.format("Database name"),'{:10.15}'.format("Quantité d'eau(%)"),'{:10.15}'.format("Glucides (%)"),'{:10.15}'.format("Lipides "),'{:10.15}'.format("sucres") , sep="\t \t")
    for names in nut_dict :
        if nut_dict[names] != []:
            for element in nut_dict[names]:

                print('{:10.15}'.format(element), end= "\t \t")
            print("")

if __name__ == "__main__":

    dico = {'boule de pâte à pizza': 1.0, 'olive': 1.0, 'boule de mozzarella': 1.0, 'origan': 1.0, 'coulis de tomate': 300.0, 'jambon cru': 4.0, 'champignon de paris': 200.0, 'pâte à pizza': 1.0, 'boules de mozzarella': 2.0, 'coulis': 300.0, 'jambon': 4.0}
    getDictNut(dico)
    output = getDictNut(dico)
    # for key in output :
    #     if output[key] != []:
    #         print(output[key])
    # print(getNutInfo("Tomate",myBook))
    # nutPrinter(output)
    getDictNutPond(dico,output)