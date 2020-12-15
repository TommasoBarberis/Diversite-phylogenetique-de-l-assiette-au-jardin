import xlrd
import csv
# name : 7 
# water % : 13
# glucides % 16
# lipides % 17 
# sucres % 18

#faire une classe ingrédient ?

def openBook(file):
    book = xlrd.open_workbook(file)
    return book

def getDefaultLineNumber(ingredient):
    f = open("nutrition_db/default.txt", "r")
    default_list = f.read().splitlines()
    for line in default_list :
        if ingredient in line : 
            value = line.split(" ")
            return int(value[1])-1
    return 0
        
def getNutInfo(ing,book):
    sheet = book.sheets()[0]
    #print(ing)
    cpt = getDefaultLineNumber(ing.lower())
    found_in_book = False
    # ing = "Pomme de terre"
    nut_info = []
    final_nut_info = []
    if cpt !=0:
        found_in_book = True
    else :
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

        final_nut_info.append(nut_info[7]) #name
        final_nut_info.append(nut_info[13]) #water
        final_nut_info.append(nut_info[16]) #glucides
        final_nut_info.append(nut_info[17]) #lipides
        final_nut_info.append(nut_info[18]) #sucres
        final_nut_info.append(nut_info[14]) #protéines

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

        qtt = str(dict_ing[ing.lower()])
        qtt  = format_float(qtt)
        wat_unpond = format_float(str(dict_nut[ing][1]))
        gluc_unpond = format_float(str(dict_nut[ing][2]))
        lip_unpond = format_float(str(dict_nut[ing][3]))
        suc_unpond = format_float(str(dict_nut[ing][4]))

        wat_pond = round(float(qtt) * float(wat_unpond)/100,2) 
        gluc_pond = round(float(qtt) * float(gluc_unpond)/100,2)
        lip_pond = round(float(qtt) * float(lip_unpond)/100,2) 
        suc_pond = round(float(qtt) * float(suc_unpond)/100,2) 
        #unités ????
        print("ingrédient : "+ ing + " og qtté = " +str(qtt) +" water_pond = " + str(wat_pond) + " gluc_pond = " + str(gluc_pond)+ " lip_pond = " + str(lip_pond)+ " suc_pond = " + str(suc_pond))

def dryMatterDicUpdate(dict_ing, dict_nut):
    dry_matter_dict = {}
    for ing in dict_ing : 
        if ing.capitalize() in dict_nut and dict_ing[ing] != 0 and dict_nut[ing.capitalize()][1] != '-':
            if "<" in dict_nut[ing.capitalize()][1] :
                wat = float(format_float(str(dict_nut[ing.capitalize()][1][2:])))
            else :
                wat = float(format_float(str(dict_nut[ing.capitalize()][1])))
            qtt = str(dict_ing[ing])
            qtt  = float(qtt)
            dry_matter = round(qtt - qtt * wat/100,2) 
            dry_matter_dict[ing] = dry_matter
        else : 
            dry_matter_dict[ing] = "NA"

    return dry_matter_dict



def format_float(input_string):
    if "-" in input_string or "traces" in input_string:
        return 0
    else :
        return input_string.replace("< ","").replace(",",".")
 


def nutPrinter(nut_dict):
    print('{:10.20}'.format("Database name"),'{:10.15}'.format("Quantité d'eau(%)"),'{:10.15}'.format("Glucides (%)"),'{:10.15}'.format("Lipides "),'{:10.15}'.format("sucres") , sep="\t \t")
    for names in nut_dict :
        if nut_dict[names] != []:
            for element in nut_dict[names]:

                print('{:10.15}'.format(element), end= "\t \t")
            print("")
    #    def writeTsv(file_name,dico_ing,dico_matier_seche, dico_nut, dico_especes): 

def writeTsv(file_name,dico_ing,dico_especes,dry_matter_dico,dico_nut):
    ing_list = list(dico_ing.keys())
    list_column=["Ingrédient","Espèce","Quantité ","Matière sèche (g)","Glucides (%)","Lipides (%)","Sucres (%)" ,"Protéines, N x facteur de Jones (%)"]
    with open(file_name, 'w', newline='') as tsvfile:
        for element in list_column :
            tsvfile.write(element)
            tsvfile.write("\t")
        tsvfile.write("\n")
        for ing in ing_list:
            tsvfile.write(ing)
            tsvfile.write("\t")
            ing_cap = ing.capitalize() 
            if ing in dico_especes :
                tsvfile.write(dico_especes[ing])
            else :
                tsvfile.write("-")
            tsvfile.write("\t")
            tsvfile.write(str(dico_ing[ing]))
            tsvfile.write("\t")
            tsvfile.write(str(dry_matter_dico[ing]))
            tsvfile.write("\t")
            if ing_cap in dico_nut :
                for i in range(2,len(dico_nut[ing_cap])) :
                    tsvfile.write(dico_nut[ing_cap][i])
                    tsvfile.write("\t")
            else :
                tsvfile.write("-\t-\t-\t-")
            tsvfile.write("\n")


if __name__ == "__main__":

    dico = {'boule de pâte à pizza': 1.0, 'olive': 1.0, 'boule de mozzarella': 1.0, 'origan': 1.0, 'coulis de tomate': 300.0, 'jambon cru': 4.0, 'champignon de paris': 200.0, 'pâte à pizza': 1.0, 'boules de mozzarella': 2.0, 'coulis': 300.0, 'jambon': 4.0}
    dicnut = getDictNut(dico)
    drymatterdico =dryMatterDicUpdate(dico,dicnut)
    print(drymatterdico)

    # for key in dicnut :
    #     print(key)
    #     print(dicnut[key])

    # print(getNutInfo("Tomate",myBook))
    # nutPrinter(output)
    # getDictNutPond(dico,output)