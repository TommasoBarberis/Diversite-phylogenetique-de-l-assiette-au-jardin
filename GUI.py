#  -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from urllib.parse import urlparse
import webbrowser
from lib import get_lifeMap_subTree, get_ing, ing_to_esp, get_dp, ing_properties
import pyperclip
from ete3 import NCBITaxa
import os
import logging


logger = logging.getLogger("GUI.py")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MainWindow:
    '''
    fenetre principale.
    lien vers les sites importantes et Entry pour entrer l'url de la recette a sousmettre.
    '''


    def __init__(self, main_window):
        self.main_window = main_window
        
    # window setting 
        main_window.title("Diversité phylogénétique de l’alimentation")
        main_window.geometry("800x740")
        main_window.minsize(800,400)
        main_window.config(background = "#2a9d8f")

    # title 
        label_title = Label(self.main_window, text = "Diversité phylogénétique \nde l’alimentation", font = 'Arial 35 bold', \
            bg = '#2a9d8f', fg = "#f0efeb")
        label_title.grid(row = 1, column = 1, pady = 10)


        def open_site (url):
            webbrowser.open_new(url)


        def underline (label):
            label.config(font = ("Arial", 20, "underline"))


        def desunderline (label):
            label.config(font = ("Arial", 20))


    # entry
        label_entry = Label(self.main_window, text = "Entrez l'url d'une recette du site marmiton:", font = ("Arial", 20, 'bold'), \
            bg = '#2a9d8f', fg = '#f0efeb')
        label_entry.grid(row = 3,column = 1, pady = 10)
        self.url_entry=Entry(self.main_window, font = ("Arial", 20), bg = '#2a9d8f', fg = '#f0efeb', width = 40)
        self.url_entry.grid(row = 4,column = 1, pady = 10)

    # submit
        submit = Button(self.main_window, text = 'Entrer', font = 'arial 20 bold', bg = '#f0efeb', fg = '#2a9d8f', \
        width = 12, command = self.test_domain)
        submit.grid(row = 5,column = 1)

    # labels (sites)
        label1 = Label(self.main_window, text = "Sites optimisés:", font = ("Arial", 22, 'bold'), bg = '#2a9d8f', fg = '#000000', justify = CENTER)
        label1.grid(row = 7, column = 1, sticky = W)
        label2 = Label(self.main_window, text = "\twww.marmiton.org", font = ("Arial", 20), bg = '#2a9d8f', fg = '#f0efeb', justify = CENTER)
        label2.grid(row = 8,column = 1, sticky = W)
        label2.bind('<Button-1>', lambda x: open_site("https://www.marmiton.org/"))
        label2.bind('<Enter>', lambda x: underline(label2))
        label2.bind('<Leave>', lambda x: desunderline(label2))

    # gitlab button
        def open_gitlab():
            webbrowser.open_new("https://gitlab.com/TommasoBarberis/diversite-phylogenetique-de-l-assiette-au-jardin")
        gitlab_button=Button(self.main_window, text = "GitLab", font = 'arial 20 bold', bg = "#f0efeb", fg = "#2a9d8f", \
        width = 10, command = open_gitlab)
        gitlab_button.grid(row = 10, column = 1)

    # ucbl button
        def open_ucbl():
            webbrowser.open_new("https://www.univ-lyon1.fr/")
        ucbl_button=Button(self.main_window, text = "UCBL", font = 'arial 20 bold', bg = '#f0efeb', fg = '#2a9d8f',\
         width = 10, command = open_ucbl)
        ucbl_button.grid(row = 12, column = 1)

    # grid
        main_window.grid_rowconfigure(0, weight = 1)
        main_window.grid_rowconfigure(2, weight = 1)
        main_window.grid_rowconfigure(6, weight = 1)
        main_window.grid_rowconfigure(9, weight = 1)
        main_window.grid_rowconfigure(11, weight = 1)
        main_window.grid_rowconfigure(13, weight = 1)

        main_window.grid_columnconfigure(0, weight = 1)
        main_window.grid_columnconfigure(2, weight = 1)


    def test_domain(self):
        '''
        pour tester si l'url est valide, si c'est le cas il ouvre une nouvelle fenetre pour 
        demander les informations manquantes ou sinon directement pour afficher les resultats,
        autrement il affiche une fenetre d'erreur.
        '''

        def open_error_window(self):
            try:
                logger.info("Open error window for incorrect url")
                self.error_window()
            except Exception:
                logger.exception("Error in 'error' window opening")


        url = self.url_entry.get()
        logger.info("URL recipe entered by the user: " + url)
        domain = ""
        try:
            domain = urlparse(url).netloc
        except Exception:
            open_error_window(self)

        if domain == "www.marmiton.org":  
            try:
                ingredients = get_ing.process(url)
            except Exception:
                self.results_window(ingredients, species)
                logger.info("Open result window")
                logger.exception("Error in the url")

            species = ing_to_esp.recherche_globale(ingredients)
            dict_nutrition = ing_properties.getDictNut(ingredients)
            dry_matter_dico = ing_properties.dryMatterDicUpdate(ingredients, dict_nutrition)


            if len(ingredients) != len(species) or len(ingredients) != len(dry_matter_dico):
                try:
                    self.missing_info_window(ingredients, species, url, dict_nutrition, dry_matter_dico)
                    logger.info("Open missing information window")
                except:
                    logger.exception("Error in 'missing information' window opening")
            else:
                try:
                    self.results_window(ingredients, species)
                    logger.info("Open result window")
                except Exception:
                    logger.exception("Error in 'result' window opening")

        else:
            open_error_window(self)



    def error_window(self):
        '''
        Ouvre la fenetre d'erreur.
        '''

        self.error = Toplevel(self.main_window)
        self.app = Error(self.error)


    def results_window(self, ingredients, species): 
        '''
        Ouvre la fenetre des resultats.
        '''  

        self.results = Toplevel(self.main_window)
        self.app = Results(ingredients, species, self.results, url_recipe = self.url_entry.get())

    def missing_info_window(self, ingredients, species, url_recipe, dict_nutrition, dry_matter_dico):
        '''
        Ouvre la fenetre pour rajouter les informations manquantes
        '''

        self.missing = Toplevel(self.main_window)
        self.app = MissingPage(ingredients = ingredients, species = species, url_recipe = url_recipe, missing_window = self.missing, dict_nutrition = dict_nutrition, dry_matter_dico = dry_matter_dico)

class Error:
    '''
    Creation de la fenetre pour le message d'erreur.
    '''


    def __init__(self, error_window):
        self.error_window = error_window
        
    # window setting 
        error_window.title("Error")
        error_window.geometry("700x200")
        error_window.minsize(700,200)
        error_window.config(background = "white")

    # label
        error_message = Label(self.error_window, text = "L’URL du site web que vous avez indiquée n’est pas valide. \nVeuillez saisir une URL correct et réessayez", \
            font = 'Arial 13 bold', bg = 'white')
        error_message.grid(row = 1, column = 1)


    # close button
        def close():
            error_window.destroy()
        close_button = Button(self.error_window, text = "Fermer", command = close)
        logger.info("The user has click to close the error window")
        close_button.grid(row = 3, column = 1)

    # grid
        error_window.grid_rowconfigure(0, weight = 1)
        error_window.grid_rowconfigure(2, weight = 1)
        error_window.grid_rowconfigure(4, weight = 1)
        error_window.grid_columnconfigure(0, weight = 1)
        error_window.grid_columnconfigure(2, weight = 1)


# Commons functions for the several windows

def updateScrollRegion(canvas, frame):
    canvas.update_idletasks()
    canvas.config(scrollregion = frame.bbox())


def createScrollableContainer(canvas, frame, x_scrollbar, y_scrollbar):
    canvas.config(xscrollcommand = x_scrollbar.set, highlightthickness = 0)      
    canvas.config(yscrollcommand = y_scrollbar.set, highlightthickness = 0)      
    x_scrollbar.config(orient = HORIZONTAL, command = canvas.xview)
    y_scrollbar.config(orient = VERTICAL, command = canvas.yview)
    x_scrollbar.pack(fill = X, side = BOTTOM, expand = FALSE)
    y_scrollbar.pack(fill = Y, side = RIGHT, expand = FALSE)
    canvas.pack(fill = BOTH, side = LEFT, expand = TRUE)
    canvas.create_window(0, 0, window = frame, anchor = NW)


def enter_button(label, text):
    label.config(text = text)

            
def leave_button(label):
    label.config(text = "")

class MissingPage:
    '''
    Creation de la fenetre pour recuperer les informations manquantes
    '''

    def __init__(self, ingredients, species, url_recipe, missing_window, dict_nutrition, dry_matter_dico):
        self.missing_window = missing_window

    # window setting 
        missing_window.title("Informations manquantes")
        missing_window.geometry("1000x740")
        missing_window.config(background = "#C8BFC7")


        container = Frame(self.missing_window, bg = "#C8BFC7")
        container.pack(side = TOP, fill = BOTH, expand = 1)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}

        for F in (MissingSpeciesPage, MissingQuantitiesPage):
            frame = F(container, self, missing_window, ingredients, species, url_recipe, dict_nutrition, dry_matter_dico)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = NSEW)

        if len(ingredients) == len(species):
            self.show_frame(MissingQuantitiesPage)
        else:
            self.show_frame(MissingSpeciesPage)
    
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        logger.info("Switch to {}".format(name.__name__))

    
def results_window_from_missing_window(self, ingredients, species, url_recipe, window, dict_nutrition, dry_matter_dico, *args): 
    '''
    Ouvre la fenetre des resultats.
    '''  

    if str(self) == ".!toplevel.!frame.!missingquantitiespage": # it modify ingredients quantities and units only if the function is called by MissingQuantitesPage
        for ind, arg in enumerate(args):
            if ind == 0:
                quantities = arg
            elif ind == 1:
                units = arg
            elif ind == 2:
                new_ing = arg

        for ind, ing in enumerate(new_ing):
            if quantities[ind].get() != "" and units[ind].get() != "": # if any quantities or units is given, the original data are conserved
                ingredients[ing] = [ingredients[ing][0], quantities[ind].get(), [units[ind].get(),units[ind].get()]]        
                logger.debug("The user add {} quantity and unit for the ingredient {}".format(str(quantities[ind].get() + " " + str(units[ind].get())), ing))

        dry_matter_dico = ing_properties.dryMatterDicUpdate(ingredients, dict_nutrition)

    self.results = Toplevel(self)
    self.app = Results(ingredients, species, self.results, url_recipe, dict_nutrition, dry_matter_dico)
    window.withdraw()


class MissingSpeciesPage(Frame):

    def __init__(self, parent, controller, window, ingredients, species, url_recipe, dict_nutrition, dry_matter_dico):
        Frame.__init__(self, parent)

        self.config(bg = "#C8BFC7")
        instruction_frame = Frame(self, bg = "#C8BFC7")
        instruction_frame.grid_columnconfigure(0, weight = 1)
        instruction_frame.grid_rowconfigure(0, weight = 1)
        instruction_label = Label(instruction_frame, text = "Si c'est possible, renseigner les \nespèces pour les ingrédients suivants:", font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
        instruction_label.grid(row = 1, column = 1, sticky = W)
        instruction_frame.grid_columnconfigure(2, weight = 1)

        entry_frame = Frame(self, bg = "#C8BFC7")
        entry_frame.grid_columnconfigure(0, weight = 1)
        entry_frame.grid_rowconfigure(0, weight = 1)
        counter_line = 3
        
        entries = []
        for ing in ingredients:
            if ing not in species:
                ing_cell = Label(entry_frame, text = ing, font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#000000")
                ing_cell.grid(row = counter_line, column = 1, sticky = E, padx = 20)

                sp_entry = Entry(entry_frame, font = "arial 11", width = 40)
                sp_entry.grid(row = counter_line, column = 3, sticky = W)

                not_valid_label = Label(entry_frame, text = "", bg = '#C8BFC7', fg = "#8A7E72", width = 30)
                not_valid_label.grid(row = counter_line, column = 5, sticky = NSEW)

                entries.append((ing, sp_entry, not_valid_label))

                counter_line += 1


        entry_frame.grid_rowconfigure(counter_line + 1, weight = 1)

        buttons_frame = Frame(self, bg = "#C8BFC7")
        buttons_frame.grid_rowconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(0, weight = 1)
        
        test_button = Button(buttons_frame, text = "Test", font = "arial 20 bold", bg = '#8A7E72', fg = "#5A2328", width = 12)
        test_button.grid(row = 1, column = 1, pady = 10, sticky = W)
        test_button.bind('<Button-1>', lambda x: test_species(entries))
        

        label_info = Label(buttons_frame, text = "", bg = '#C8BFC7', fg = "#8A7E72", width = 50)
        label_info.grid(row = 1, column = 3, sticky = NSEW)
        test_button.bind('<Enter>', lambda x: enter_button(label_info, 'Permet de tester si les espèces rentrées \nsont des noms taxonomiques valides'))
        test_button.bind('<Leave>', lambda x: leave_button(label_info))

        next_button = Button(buttons_frame, text = "Suivant", font = "arial 20 bold", bg = '#8A7E72', fg = "#5A2328", width = 12)
        finish_button = Button(buttons_frame, text = "Suivant", font = "arial 20 bold", bg = '#8A7E72', fg = "#5A2328", width = 12)

        if len(ingredients) != len(dry_matter_dico):
            next_button.grid(row = 3, column = 1, pady = 10, sticky = W)
            next_button.bind('<Button-1>', lambda x: controller.show_frame(MissingQuantitiesPage))
        else:
            finish_button.grid(row = 3, column = 1, pady = 10, sticky = W)
            next_button.bind('<Button-1>', lambda x: results_window_from_missing_window(self.ingredients, species, url_recipe, window, dict_nutrition, dry_matter_dico))


        def test_species(entries):
            '''
            Permet de tester si les espèces rentrées par l'utilisateur sont des noms taxonomiques valides
            '''
            
            for entry in entries:
                if entry != "":
                    logger.debug("The user has enter '{}' for the ingredient '{}'".format(entry[1].get(), entry[0]))
                sp = get_lifeMap_subTree.get_taxid({entry: entry[1].get()})

                if sp != []:
                    species[entry[0]] = entry[1].get()
                    entry[2].config(text = "")

                    with open("data/filtered_scientific_name_db.txt", "a") as name_db:
                        new_line = str(entry[1].get()) + "\t" + str(entry[0] + "\n")
                        name_db.write(new_line)

                    with open("data/filtered_scientific_name_db.txt", "r") as name_db:
                        lines = name_db.readlines()

                    with open("data/filtered_scientific_name_db.txt", "w") as name_db:

                        # conserving unique lines
                        for line in lines:
                            if lines.count(line) > 1:
                                for i in range(lines.count(line)):
                                    lines.pop(lines.index(line))
                        
                        # sorting lines
                        lines.sort()

                        for line in lines:
                            name_db.write(line)

                else:
                    entry[2].config(text = "Nom taxonomique non valide")


        instruction_frame.pack(side = TOP, fill = X, expand = 1,  anchor = CENTER)
        entry_frame.pack(side = TOP, fill = X, expand = 1, anchor = CENTER)
        buttons_frame.pack(side = TOP, fill = X, expand = 1, anchor = CENTER)


class MissingQuantitiesPage(Frame):

    def __init__(self, parent, controller, window, ingredients, species, url_recipe, dict_nutrition, dry_matter_dico):
        Frame.__init__(self, parent)
        self.config(bg = "#C8BFC7")

        instruction_frame = Frame(self, bg = "#C8BFC7")
        instruction_label = Label(instruction_frame, text = "Si c'est possible, renseigner les quantités \npour les ingrédients suivants ainsi que leurs unités de mesure:", font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
        instruction_label.pack(side = TOP, fill = BOTH, expand = 1, anchor = CENTER)
        instruction_frame.pack(side = TOP, fill = BOTH, expand = 1, anchor = CENTER)

        data_frame = Frame(self, bg = "#C8BFC7")
        data_frame.grid_columnconfigure(0, weight = 1)
        data_frame.grid_rowconfigure(0, weight = 1)
        counter_line = 3
        
        quantities = []
        units = []
        new_ing = []

        for ing in ingredients:
            if ing not in dry_matter_dico:
                ing_label = Label(data_frame, text = ing, font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#000000")
                ing_label.grid(row = counter_line, column = 1, sticky = E, padx = 20)

                quantity_entry = Entry(data_frame, font = "arial 11", width = 40)
                quantity_entry.grid(row = counter_line, column = 3, sticky = W)
                quantities.append(quantity_entry)

                unit_choice = ttk.Combobox(data_frame, width = 10)
                unit_choice['values'] = ('g', 'kg', 'cl', 'dl', 'l')
                unit_choice.grid(row = counter_line, column = 5, sticky = E, padx = 20)
                units.append(unit_choice)

                new_ing.append(ing)
                counter_line += 1
        
        data_frame.grid_columnconfigure(6, weight = 1)
        data_frame.pack(side = TOP, fill = BOTH, expand = 1, anchor = CENTER)

        buttons_frame = Frame(self, bg = "#C8BFC7")
        buttons_frame.grid_rowconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(0, weight = 1)

        prev_button = Button(buttons_frame, text = "Avant", font = 'arial 20 bold', bg = '#8A7E72', fg = '#5A2328', width = 12)
        buttons_frame.grid_columnconfigure(2, weight = 1)
        
        if len(ingredients) != len(species):
            prev_button.grid(row = 1, column = 1, pady = 10, sticky = W)

        prev_button.bind('<Button-1>', lambda x: controller.show_frame(MissingSpeciesPage))

        finish_button = Button(buttons_frame, text = "Terminer", font = 'arial 20 bold', bg = '#8A7E72', fg = '#5A2328', width = 12)
        finish_button.grid(row = 1, column = 3, pady = 10, sticky = W)
        finish_button.bind('<Button-1>', lambda x: results_window_from_missing_window(self, ingredients, species, url_recipe, window, dict_nutrition, dry_matter_dico, quantities, units, new_ing))
        buttons_frame.grid_columnconfigure(4, weight = 1)


        buttons_frame.pack(side = TOP, fill = X, expand = 1, anchor = CENTER)


class Results:
    '''
    Creation de la fenetre pour les résultats.
    '''

    def __init__(self, ingredients, species, results_window, url_recipe, dict_nutrition, dry_matter_dico):
        self.results_window = results_window
        self.url_recipe = url_recipe

    # window setting 
        results_window.title("Résultats")
        # w = results_window.winfo_screenwidth()
        # h = results_window.winfo_screenheight()
        # results_window.geometry("%dx%d+0+0" % (w, h))
        results_window.geometry("1800x800")
        results_window.minsize(1080, 720)
        results_window.config(background = "#C8BFC7")
        results_window.grid_columnconfigure(0, weight = 1)

    # Main canvas
        self.main_canvas = Canvas(self.results_window, bg = "#C8BFC7")
        main_frame = Frame(self.main_canvas, bg = "#C8BFC7")
        y_scrollbar = Scrollbar(self.main_canvas)
        x_scrollbar = Scrollbar(self.main_canvas)


    #some functions
        def open_site (url):
            webbrowser.open_new(url)


        def underline (label):
            label.config(font = ("Arial", 18, "underline"))


        def desunderline (label):
            label.config(font = ("Arial", 18))


    # recipe's name 
        name_recipe = get_ing.get_title(self.url_recipe)
        label1 = Label(main_frame, text = "Nom de la recette: ", font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
        label1.grid(row = 1, column = 1, sticky = W, columnspan = 6)
        recipe = Label(main_frame, text = name_recipe, font = 'Arial 18', bg = '#C8BFC7', fg = "#000000", justify = CENTER)
        recipe.grid(row = 1, column = 3, sticky = W, columnspan = 6)
    
    # missing species
        string1="{} espèces ont été trouvé pour les {} ingrédients.".format(len(species), len(ingredients))
        missing_species1 = Label(main_frame, text = string1, font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
        missing_species1.grid(row = 3, column = 1, sticky = W, columnspan = 6)
        missing_sp_list = missing_species(ingredients, species)

        save_row = 5

        if not missing_sp_list[1]:
            missing_species2 = Label(main_frame, text = "Les ingrédients pour lesquels l’espèce manque:", \
                font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
            missing_species2.grid(row = 4, column = 1, sticky = W, columnspan = 6)
            for add, sp in enumerate(missing_sp_list[0]):
                save_row += add
                missing = Label(main_frame, text = "\t"+sp, font = 'Arial 18', bg = '#C8BFC7', fg = "#000000")
                missing.grid(row = save_row, column = 1, sticky = W, columnspan = 6)
        else:
            not_missing = Label(main_frame, text = "Aucune espèce manque", font = 'Arial 18', bg = '#C8BFC7', \
            fg = "#000000").grid(row = save_row, column = 1, sticky = W, columnspan = 6)

    # missing ingredients in nutritional db
        missing_ing_list = missing_nutrition(ingredients, dict_nutrition)
        string2="{}/{} ingrédients ont été trouvé dans la table Ciqual (base de données).".format(str(len(ingredients) \
            - len(missing_ing_list[0])),len(ingredients))
        missing_ing1 = Label(main_frame, text = string2, font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
        save_row+=1
        missing_ing1.grid(row = save_row, column = 1, sticky = W, columnspan = 6)
        if not missing_ing_list[1]: 
            missing_ing2 = Label(main_frame, text = "Ingrédients pour lesquels aucune information a été trouvé:", \
                font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
            save_row += 1
            missing_ing2.grid(row = save_row, column = 1, sticky = W, columnspan = 6)
            save_row += 1
            for add1, ing in enumerate(missing_ing_list[0]):
                save_row += add1
                missing1 = Label(main_frame, text = "\t"+ing, font = 'Arial 18', bg = '#C8BFC7', fg = "#000000")
                missing1.grid(row = save_row, column = 1, sticky = W, columnspan = 6)

    # table
        dict_row = table_row(ingredients, species, dict_nutrition, dry_matter_dico)
        list_column = ["Ingrédient", "Espèce", "Quantité", "Qté de matière\n sèche (g)", "Eau (%)", \
            "Glucides (%)", "Lipides (%)", "Protéines (%)"]
        save_row += 1

        for i in range(len(list_column)):
            if i == 2:
                table_header = Label(main_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = CENTER, relief = GROOVE, width = 14, height = 3)
            elif i == 3:
                table_header = Label(main_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = CENTER, relief = GROOVE, width = 16, height = 3)
            elif i == 4:
                table_header = Label(main_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = CENTER, relief = GROOVE, width = 14, height = 3)
            elif i == 5:
                table_header = Label(main_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = CENTER, relief = GROOVE, width = 14, height = 3)
            elif i == 6:
                table_header = Label(main_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = CENTER, relief = GROOVE, width = 13, height = 3)
            else:
                table_header = Label(main_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = CENTER, relief = GROOVE, width = 18, height = 3) 

            table_header.grid(row = save_row, column = 1+i, sticky = W)

        for j in dict_row.keys():
            line = dict_row[j]
            save_row += 1
            for ind, k in enumerate(line):
                if ind == 2:
                    table_cell = Label(main_frame, text = k[1]+" "+k[2][1], font = "Arial 14", bg = '#C8BFC7', \
                    fg = "#000000", justify = CENTER, relief = GROOVE, width = 14, wraplength = 300, height = 2)
                elif ind == 3:
                    table_cell = Label(main_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = CENTER, relief = GROOVE, width = 16, wraplength = 300, height = 2)
                elif ind == 4:
                    table_cell = Label(main_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = CENTER, relief = GROOVE, width = 14, wraplength = 300, height = 2)
                elif ind == 5:
                    table_cell = Label(main_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = CENTER, relief = GROOVE, width = 14, wraplength = 300, height = 2)
                elif ind == 6:
                    table_cell = Label(main_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = CENTER, relief = GROOVE, width = 13, wraplength = 300, height = 2)
                else:
                    table_cell = Label(main_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = CENTER, relief = GROOVE, width = 18, wraplength = 300, height = 2)
                table_cell.grid(row = save_row, column = 1 + ind, sticky =W)

        save_row += 2
    
    # buttons


        def enter_download(label_photo_info):
            label_photo_info.config(text = 'Télécharger le tableau au format tsv')
        
        
        def leave_download(label_photo_info):
            label_photo_info.config(text = "")


        photo = PhotoImage(file = r"assets/download_arrow.png")
        sub_photo = photo.subsample(7, 7)
        download = Button(main_frame, image = sub_photo,  bg = '#8A7E72', width = 40, height = 40, \
        command = self.download_button)
        download.image = sub_photo
        label_photo_info = Label(main_frame, text = "", bg = '#C8BFC7', fg = "#8A7E72")
        label_photo_info.grid(row = save_row, column = 1, columnspan = 2, sticky = N)
        download.grid(row = save_row - 1, column = 0, pady = 10, columnspan = 3)
        download.bind('<Enter>', lambda x: enter_download(label_photo_info))
        download.bind('<Leave>', lambda x: leave_download(label_photo_info))


        def get_lifemap (species):
            get_lifeMap_subTree.get_subTree(species)
            logger.info("Opening LifeMap page")
        lifemap = Button(main_frame, text = "LifeMap Tree", font = "arial 20 bold", bg = '#8A7E72', \
        fg = "#5A2328", width = 12)
        lifemap.grid(row = save_row, column = 3, pady = 10, sticky = W, columnspan = 2)
        lifemap.bind('<Button-1>', lambda x: get_lifemap(species))
        
        save_row += 1

        list_ID = get_lifeMap_subTree.get_taxid(species)
        ncbi = NCBITaxa()
        tree = ncbi.get_topology((list_ID), intermediate_nodes = True)
        tree = tree.write(format = 100, features = ["sci_name"]).replace('[&&NHX:sci_name=', '').replace(']', '')

        
        tree_file = ncbi.get_topology((list_ID), intermediate_nodes = False)
        tree_file = tree_file.write(format = 100, features = ["sci_name"]).replace('[&&NHX:sci_name=', '').replace(']', '')

        try:
            os.remove("Tree.txt")
        except Exception:
            pass
        with open("Tree.txt","w") as Tree:
            Tree.write(tree_file)
            logger.info("Writing Tree.txt")


        def get_ete(tree):
            try:
                get_lifeMap_subTree.subtree_from_newick(tree)
                logger.info("The user has click the ete's button")
            except Exception:
                logger.exception("Ete browser doesn't work")


        ete = Button(main_frame, text = "Ete Sub-tree", font = "arial 20 bold", bg = '#8A7E72', \
        fg = "#5A2328", width = 12)
        ete.grid(row = save_row, column = 3, pady = 10, sticky = W, columnspan = 2)
        ete.bind('<Button-1>', lambda x: get_ete(tree_file))

        save_row += 1


        def get_newick(tree):
            pyperclip.copy(tree)
            logger.info("The user has click the newick's button")

        newick = Button(main_frame, text = "Newick Tree", font = "arial 20 bold", bg = '#8A7E72', fg = "#5A2328", width = 12)
        newick.grid(row = save_row, column = 3, pady = 10, sticky = W, columnspan = 2)
        newick.bind('<Button-1>', lambda x: get_newick(tree_file))


        label_info = Label(main_frame, text = "", bg = '#C8BFC7', fg = "#8A7E72", width = 40)
        label_info.grid(row = save_row + 1, column = 4, columnspan = 3, sticky = NSEW)
        newick_info = Button(main_frame, text = "?", font = "arial 20 bold", bg = '#8A7E72', \
        fg = "#5A2328", width = 2)
        newick_info.grid(row = save_row, column = 4, pady = 10, sticky = E)
        newick_info.bind('<Enter>', lambda x: enter_button(label_info, 'Le bouton "Newick Tree" \npermet de recopier le sous-arbre \nde newick dans le clipboard'))
        newick_info.bind('<Leave>', lambda x: leave_button(label_info))

        # DP
        dp = get_dp.phylogenetic_diversity(tree, species)
        label6 = Label(main_frame, text = "Diversité phylogénétique (en nb de branches):", \
            font = 'Arial 14 bold', bg = '#C8BFC7', fg = "#8A7E72", justify = CENTER)
        label6.grid(row = save_row - 2, column = 5, columnspan = 4, sticky = NSEW)
        dp_label = Label(main_frame, text = dp, font = 'Arial 18 bold', bg = '#C8BFC7', \
        fg = "#090302", justify = CENTER, relief = RAISED, width = 7, height = 3)
        dp_label.grid(row = save_row - 1, column = 5, columnspan = 4)

        dictionnaire_nutrition = ing_properties.getDictNut(ingredients)
        drym_dict = ing_properties.dryMatterDicUpdate(ingredients, dictionnaire_nutrition)
        dict_sp_drym = {}
        bool_var = TRUE
        for sp in species.keys():
            if sp in drym_dict.keys():
                dict_sp_drym[species[sp]] = drym_dict[sp]
            else:
                bool_var = FALSE
                break
        
        if bool_var is TRUE:
            wdp = get_dp.weighted_phylogenetic_diversity(tree, species, dict_sp_drym)
        else:
            wdp = "NA"
        
        label7 = Label(main_frame, text = "Diversité phylogénétique pondérée:", font = 'Arial 14 bold', \
            bg = '#C8BFC7', fg = "#8A7E72", justify = CENTER)
        label7.grid(row = save_row, column = 5, columnspan = 4, sticky = NSEW)
        wdp_label = Label(main_frame, text = wdp,  font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#090302", \
        justify = CENTER, relief = RAISED, width = 7, height = 3)
        wdp_label.grid(row = save_row + 1, column = 5, columnspan = 4)

    # grid
        results_window.rowconfigure(0, weight = 1)
        results_window.rowconfigure(save_row + 1, weight = 1)

        results_window.grid_columnconfigure(8, weight = 1)

        main_frame.pack()
        self.main_canvas.pack()
        updateScrollRegion(self.main_canvas, main_frame)
        createScrollableContainer(self.main_canvas, main_frame, x_scrollbar, y_scrollbar)

    # Mousewheel
        self.results_window.bind('<Button-4>', lambda event: self.main_canvas.yview('scroll', -1, 'units'))
        self.results_window.bind('<Button-5>', lambda event: self.main_canvas.yview('scroll', 1, 'units'))
        self.results_window.bind('<MouseWheel>', lambda event: self.main_canvas.yview('scroll', 1, 'units'))
        self.results_window.bind('<MouseWheel>', lambda event: self.main_canvas.yview('scroll', -1, 'units'))


    def download_button (self):
        self.file_name_window()
        logger.info("The user has click the download button for the tsv table")


    def file_name_window(self):
        '''
        Ouvre la fenetre pour nommer le fichier qui aura le tableau au format tsv.
        '''
        self.download = Toplevel(self.results_window)
        self.app = Download(self.download, url_recipe=self.url_recipe)


class Download:
    '''
    Creation de la fenetre qui permet de rentrer le nom du fichier dans lequel on souhaite telecharger le tableau au format csv ou tsv.
    '''
    def __init__(self, download_window, url_recipe):
        self.download_window = download_window
        self.url_recipe = url_recipe
        
    # window setting 
        download_window.title("Enregistrement")
        download_window.geometry("700x200")
        download_window.minsize(800, 200)
        download_window.config(background = "#C8BFC7")
        download_window.grid_rowconfigure(0, weight = 1)

    # introducing label
        intro_label = Label(self.download_window, text = "Le fichier sera enregistré dans le répertoire contenant le programme au format tsv.\nChoississez le nom du fichier:", \
                font = "arial 11",foreground = "black", bg = "#C8BFC7", justify = CENTER)
        intro_label.grid(row = 1, column = 1)
    # file name entry
        file_name = Entry(self.download_window, font = "arial 11", width = 40)
        file_name.grid(row = 2, column = 1)

        download_window.grid_rowconfigure(3, weight = 1)

    # confirm button

        def action (file_name):
            file_name = file_name.get()
            if not file_name.endswith(".tsv"):
                file_name += ".tsv"
            logger.info("TSV table saved with the filename: " + file_name)
            ing_properties.writeTsv(file_name,ingredients, species, dry_matter_dico, dict_nutrition)
            self.download_window.destroy()
        confirm_button=Button(self.download_window, text = "Enregistrer", font  = "arial 11", width = 10)
        confirm_button.grid(row = 4, column = 1)
        confirm_button.bind("<Button-1>", lambda x: action(file_name))

        download_window.grid_rowconfigure(5, weight = 1)
        download_window.grid_columnconfigure(0, weight = 1)
        download_window.grid_columnconfigure(2, weight = 1)


def missing_species(ingredients, species):
    """
    Permet de trouver les ingredients pour lesquels on a pas une espece.
    """

    species_not_found = []
    if len(ingredients) != len(species) :
        complete_spec = False
        for key in ingredients:
            if key not in species and key[:-1] not in species.keys():
                species_not_found.append(key)
    else:
        complete_spec = True
    return (species_not_found, complete_spec)


def missing_nutrition (ingredients, dict_nut):
    """
    Permet de trouver les ingredients qui ne sont pas trouve dans la table Ciqual.
    """
    nbnut = len(dict_nut)
    nut_not_found = []
    if len(ingredients) != nbnut :
        complete_nut = False
        for key in ingredients:
            if key.capitalize() not in dict_nut:
                nut_not_found.append(key.capitalize())
    else:
        complete_nut = True
    return (nut_not_found, complete_nut)


def table_row(ingredients, especes, dict_nut, dry_matter_dict):
    dict_row = {}
    for key in ingredients.keys():
        ing = ingredients[key][0]
        list_row = [ing[0]]

        if ing[0] in especes.keys():
            list_row.append(especes[ing[0]])
        elif ing[0] in especes.keys():
            list_row.append(especes[ing[0]]) 
        else:
            list_row.append("-")

        list_row.append(ingredients[key])

        if ing[0] in dry_matter_dict.keys():
            list_row.append(dry_matter_dict[ing[0]])
        elif ing[1]in dry_matter_dict.keys():
            list_row.append(dry_matter_dict[ing[1]])
        else:
            list_row.append("-")

        if str(key).capitalize() in dict_nut.keys():
            for i, val in enumerate(dict_nut[str(key).capitalize()]):
                if i == 0:
                    pass
                else:
                    list_row.append(val)
        else:
            for k in range(4):
                list_row.append("-")

        dict_row[ing[0]] = list_row
    return dict_row

def main(): 
    root = Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Error in the main program")


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
except Exception:
    pass
