#  -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import ImageTk, Image
from urllib.parse import urlparse
import webbrowser
from lib import get_lifeMap_subTree, get_ing, ing_to_esp, get_dp, ing_properties
import pyperclip
from ete3 import NCBITaxa
import os
import logging
import sys

ctk.set_appearance_mode("System")

logger = logging.getLogger("GUI.py")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MainWindow(tk.Tk):
    '''
    fenetre principale.
    lien vers les sites importantes et Entry pour entrer l'url de la recette a sousmettre.
    '''

    def __init__(self):
        tk.Tk.__init__(self)

    # window setting 
        self.title("Diversité phylogénétique de l’alimentation")
        w = 800
        h = 550
        x = (self.winfo_screenwidth() - w) / 2
        y = (self.winfo_screenheight() - h) / 2
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.minsize(800,400)
        self.config(background = "#2a9d8f")

        self.main_frame = ctk.CTkFrame(master = self, bg = "#2a9d8f", fg_color = "#2a9d8f") 

    # title 
        label_title = tk.Label(self.main_frame, text = "Diversité phylogénétique \nde l’alimentation", font = ('Montserrat', 35, 'bold'), \
            bg = '#2a9d8f', fg = "#f0efeb")
        label_title.pack(side = "top", fill = "x", expand = 1, anchor = "center")


    # entry
        label_entry = tk.Label(self.main_frame, text = "Entrez l'url d'une recette du site marmiton:", font = ("Open Sans", 20, 'bold'), \
            bg = '#2a9d8f', fg = '#f0efeb')
        label_entry.pack(side = "top", fill = "x", expand = 1, anchor = "center") 
        
        self.url_entry = ctk.CTkEntry(master = self.main_frame, font = ("Arial", 20), bg = '#2a9d8f', fg = '#f0efeb', width = 600, height = 50)
        self.url_entry.pack(side = "top", expand = 1, anchor = "n")


    # submit
        self.submit = ctk.CTkButton(master = self.main_frame, text = 'Entrer', bg_color = "#2a9d8f", \
        fg_color = "#f0efeb", command = self.test_domain, width = 200, height = 40, \
        corner_radius = 20, text_font = ("Open Sans", 20, "bold"), hover_color = "#B7B7A4", \
        text_color = "#5aa786")
        self.submit.pack(side = "top", expand = 1, anchor = "n") 
  

    #  utility buttons
        bottom_frame = tk.Frame(self, bg = "#2a9d8f")
        button_frame = ctk.CTkFrame(master = bottom_frame, bg = "#2a9d8f", fg_color = "#2a9d8f", height = 50, width = 800)

        # gitlab button     
        def open_gitlab():
            webbrowser.open("https://gitlab.com/TommasoBarberis/diversite-phylogenetique-de-l-assiette-au-jardin", new = 2)

        gitlab_icon = tk.PhotoImage(file = r"assets/gitlab.png").subsample(5, 5)
        gitlab_button = ctk.CTkButton(master =button_frame, bg_color = "#2a9d8f", fg_color = "#f0efeb", \
            text= "", width = 50, height = 50, corner_radius = 5, \
            image = gitlab_icon, hover_color = "#B7B7A4", command = open_gitlab)
        gitlab_button.pack(side = "left", expand = 0, anchor = "sw", padx = 15, pady = 10) 

        # ucbl button
        def open_ucbl():
            webbrowser.open("https://www.univ-lyon1.fr/", new = 2)

        ucbl_icon = tk.PhotoImage(file = r"assets/ucbl.png").subsample(5, 5)
        ucbl_button = ctk.CTkButton(master =button_frame, bg_color = "#2a9d8f", fg_color = "#f0efeb", \
            text= "", width = 50, height = 50, corner_radius = 5, \
            image = ucbl_icon, hover_color = "#B7B7A4", command = open_ucbl)
        ucbl_button.pack(side = "left", expand = 0, anchor = "sw", padx = 15, pady = 10)

        # marmitton button
        def open_marmiton():
            webbrowser.open("https://www.marmiton.org/", new = 2)

        marmiton_icon = tk.PhotoImage(file = r"assets/marmiton.png").subsample(7, 7)
        marmiton_button = ctk.CTkButton(master =button_frame, bg_color = "#2a9d8f", fg_color = "#f0efeb", \
            text= "", width = 50, height = 50, corner_radius = 5, \
            image = marmiton_icon, hover_color = "#B7B7A4", command = open_marmiton)
        marmiton_button.pack(side = "left", expand = 0, anchor = "sw", padx = 15, pady = 10)

    # logo
        self.logo = Image.open(r"assets/logo.png")
        self.logo = self.logo.resize((200, 200), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(bottom_frame, image = self.logo, bg = "#2a9d8f")

        self.main_frame.pack(side = "top", fill = "both", expand = 1, anchor = "center")
        bottom_frame.pack(side = "bottom", fill = "both", expand = 1)
        button_frame.pack(side = "left", fill = "both", expand = 1, anchor = "s")
        self.logo_label.pack(side = "right", padx = 20, anchor = "center")


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
            logger.info("The {} URL is invalid".format(url))

        if domain == "www.marmiton.org":  
            
            try:
                ingredients = get_ing.process(url)
                assert ingredients is not None
            except AssertionError as err:
                logger.exception(err)
                logger.error("Parse error")
                sys.exit()
                self.destroy()

            species = ing_to_esp.recherche_globale(ingredients)
            dict_nutrition = ing_properties.get_dict_nut(ingredients)
            dry_matter_dico = ing_properties.dry_matter_dict_update(ingredients, dict_nutrition)
            logger.info("URL processed, getting ingredient, species, nutrition data and dry matter information")


            if len(ingredients) != len(species) or len(ingredients) != len(dry_matter_dico):
                try:
                    self.missing_info_window(ingredients, species, url, dict_nutrition, dry_matter_dico)
                    logger.info("Open missing information window")
                except:
                    logger.exception("Error in 'missing information' window opening")
            else:
                try:
                    self.results_window(ingredients, species, url, dict_nutrition, dry_matter_dico)
                    logger.info("Open result window")
                except Exception:
                    logger.exception("Error in 'result' window opening")

        else:
            open_error_window(self)



    def error_window(self):
        '''
        Ouvre la fenetre d'erreur.
        '''

        self.error = tk.Toplevel(self)
        self.app = ErrorWin(self.error)

    def results_window(self, ingredients, species, dict_nutrition, dry_matter_dico): 
        '''
        Ouvre la fenetre des resultats.
        '''  

        self.results = tk.Toplevel(self)
        self.app = Results(ingredients, species, self.results, self.url_entry.get(), dict_nutrition, dry_matter_dico)

    def missing_info_window(self, ingredients, species, url_recipe, dict_nutrition, dry_matter_dico):
        '''
        Ouvre la fenetre pour rajouter les informations manquantes
        '''

        self.missing = tk.Toplevel(self)
        self.app = MissingPage(ingredients = ingredients, species = species, url_recipe = url_recipe, missing_window = self.missing, dict_nutrition = dict_nutrition, dry_matter_dico = dry_matter_dico)

class ErrorWin:
    '''
    Creation de la fenetre pour le message d'erreur.
    '''


    def __init__(self, error_window):
        self.error_window = error_window
        
    # window setting 
        self.error_window.title("Error")
        self.error_window.config(background = "#2a9d8f")
        w = 700
        h = 200
        x = (self.error_window.winfo_screenwidth() - w) / 2
        y = (self.error_window.winfo_screenheight() - h) / 2
        self.error_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.error_window.minsize(700,200)

        main_frame = tk.Frame(self.error_window, bg = "#2a9d8f")
    # label
        error_message = tk.Label(main_frame, text = "L’URL du site web que vous avez indiquée n’est pas valide. \nVeuillez saisir une URL correct et réessayez", \
            bg = "#2a9d8f", fg = "#f0efeb", font = ("Open Sans", 14))
        error_message.pack(side = "top", expand = 1)
        
        # close button
        def close():
            logger.info("The user has click to close the error window")
            self.error_window.withdraw()

        close_button = ctk.CTkButton(master = main_frame, text = "Fermer",\
        text_font = ("Open Sans", 15, "bold"), width = 100, height = 40, \
        command = close, bg_color = "#2a9d8f", fg_color = "#f0efeb", hover_color = "#B7B7A4", \
        text_color = "#5aa786", corner_radius = 20)
        
        close_button.pack(side = "top", expand = 1, anchor = "center", pady = 20)
        main_frame.pack(side = "top", expand = 1, anchor = "center")


# Commons functions for the several windows

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
        w = 1000
        h = 740
        x = (missing_window.winfo_screenwidth() - w) / 2
        y = (missing_window.winfo_screenheight() - h) / 2
        missing_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        missing_window.minsize(800,400)
        missing_window.config(background = "#2a9d8f")


        container = tk.Frame(self.missing_window, bg = "#2a9d8f")
        container.pack(side = "top", fill = "both", expand = 1)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}

        for F in (MissingSpeciesPage, MissingQuantitiesPage):
            frame = F(container, self, missing_window, ingredients, species, url_recipe, dict_nutrition, dry_matter_dico)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

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

        dry_matter_dico = ing_properties.dry_matter_dict_update(ingredients, dict_nutrition)

    self.results = tk.Toplevel(self)
    self.app = Results(ingredients, species, self.results, url_recipe, dict_nutrition, dry_matter_dico)
    window.withdraw()


class MissingSpeciesPage(tk.Frame):

    def __init__(self, parent, controller, window, ingredients, species, url_recipe, dict_nutrition, dry_matter_dico):
        tk.Frame.__init__(self, parent)

        self.config(bg = "#2a9d8f")
        instruction_frame = tk.Frame(self, bg = "#2a9d8f")
        instruction_frame.grid_columnconfigure(0, weight = 1)
        instruction_frame.grid_rowconfigure(0, weight = 1)
        instruction_label = tk.Label(instruction_frame, \
            text = "Si c'est possible, renseigner les \nespèces pour les ingrédients suivants:", \
                font = ("Open Sans", 18), bg = '#2a9d8f', fg = "#f0efeb")
        instruction_label.grid(row = 1, column = 1, sticky = "w")
        instruction_frame.grid_columnconfigure(2, weight = 1)

        entry_frame = tk.Frame(self, bg = "#2a9d8f")
        entry_frame.grid_columnconfigure(0, weight = 1)
        entry_frame.grid_rowconfigure(0, weight = 1)
        counter_line = 3
        
        entries = []
        for ing in ingredients:
            if ing not in species:
                ing_cell = tk.Label(entry_frame, text = ing, font = ("Open Sans", 16, "bold"), bg = '#2a9d8f', fg = "#f0efeb")
                ing_cell.grid(row = counter_line, column = 1, sticky = "e", padx = 20)

                sp_entry = ctk.CTkEntry(entry_frame, font = ("Arial", 10), width = 500, corner_radius = 10)
                sp_entry.grid(row = counter_line, column = 3, sticky = "w")

                not_valid_label = tk.Label(entry_frame, text = "", font = ("Open Sans", 10, "bold"), bg = '#2a9d8f', fg = "#f0efeb", width = 30)
                not_valid_label.grid(row = counter_line, column = 5, sticky = "nsew")

                entries.append((ing, sp_entry, not_valid_label))

                counter_line += 1


        entry_frame.grid_rowconfigure(counter_line + 1, weight = 1)


        test_button_frame = ctk.CTkFrame(master = self, bg = "#2a9d8f", fg_color = "#2a9d8f")

        def test_button_func():
            test_species(entries)

        test_button = ctk.CTkButton(master = test_button_frame, text = "Test", text_font = ("Open Sans", 20, "bold"), \
        bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
        height = 40, corner_radius = 20, command = test_button_func)    
        test_button.pack(side = "top", anchor = "n")
 
        
        # TODO - label that explain the button function
        # label_info = tk.Label(buttons_frame, text = "", bg = '#2a9d8f', fg = "#8A7E72", width = 50)
        # label_info.grid(row = 1, column = 3, sticky = "nsew")
        # test_button.bind('<Enter>', lambda x: enter_button(label_info, 'Permet de tester si les espèces rentrées \nsont des noms taxonomiques valides'))
        # test_button.bind('<Leave>', lambda x: leave_button(label_info))

        final_buttons_frame = ctk.CTkFrame(master = self, bg = "#2a9d8f", fg_color = "#2a9d8f")

        def next_button_func():
            controller.show_frame(MissingQuantitiesPage)

        next_button = ctk.CTkButton(master = final_buttons_frame, text = "Suivant", text_font = ("Open Sans", 20, "bold"), \
        bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
        height = 40, corner_radius = 20, command = next_button_func)

        def finish_button_func():
            results_window_from_missing_window(self, ingredients, species, url_recipe, window, dict_nutrition, dry_matter_dico)

        finish_button = ctk.CTkButton(master = final_buttons_frame, text = "Terminer", text_font = ("Open Sans", 20, "bold"), \
        bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
        height = 40, corner_radius = 20, command = finish_button_func)

        decisional_bool = FALSE
        for qty in dry_matter_dico.values():
            if qty == "-":
                decisional_bool = TRUE

        if decisional_bool:
            next_button.pack(side = "bottom", anchor = "se", padx = 10, pady = 10)
        else:
            finish_button.pack(side = "bottom", anchor = "se", padx = 10, pady = 10)


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


        instruction_frame.pack(side = "top", fill = "x", expand = 1,  anchor = "center")
        entry_frame.pack(side = "top", fill = "x", expand = 1, anchor = "center")
        test_button_frame.pack(side = "top", fill = "x", expand = 1, anchor = "n")
        final_buttons_frame.pack(side = "top", fill = "x", expand = 1, anchor = "se")

        w = 1000
        h = instruction_frame.winfo_reqheight() + entry_frame.winfo_reqheight() + test_button_frame.winfo_reqheight() + final_buttons_frame.winfo_reqheight()
        x = (window.winfo_screenwidth() - w) / 2
        y = (window.winfo_screenheight() - h) / 2 - 150
        window.geometry("%dx%d+%d+%d" % (w, h, x, y))


class MissingQuantitiesPage(tk.Frame):

    def __init__(self, parent, controller, window, ingredients, species, url_recipe, dict_nutrition, dry_matter_dico):
        tk.Frame.__init__(self, parent)
        self.config(bg = "#2a9d8f")

        instruction_frame = tk.Frame(self, bg = "#2a9d8f")
        instruction_label = tk.Label(instruction_frame, text = "Si c'est possible, renseigner les quantités \npour les ingrédients suivants ainsi que leurs unités de mesure:", font = 'Arial 18 bold', bg = '#2a9d8f', fg = "#8A7E72")
        instruction_label.pack(side = "top", fill = "both", expand = 1, anchor = "center")
        instruction_frame.pack(side = "top", fill = "both", expand = 1, anchor = "center")

        data_frame = tk.Frame(self, bg = "#2a9d8f")
        data_frame.grid_columnconfigure(0, weight = 1)
        data_frame.grid_rowconfigure(0, weight = 1)
        counter_line = 3
        
        quantities = []
        units = []
        new_ing = []

        for ing in ingredients:
            print(ing)
            if ing not in dry_matter_dico or ing[2][0] != "g":
                print(ing)
                ing_label = tk.Label(data_frame, text = ing, font = 'Arial 18 bold', bg = '#2a9d8f', fg = "#000000")
                ing_label.grid(row = counter_line, column = 1, sticky = "e", padx = 20)

                quantity_entry = tk.Entry(data_frame, font = "arial 11", width = 40)
                quantity_entry.grid(row = counter_line, column = 3, sticky = "w")
                quantities.append(quantity_entry)

                unit_choice = ttk.Combobox(data_frame, width = 10)
                unit_choice['values'] = ('g', 'kg', 'cl', 'dl', 'l')
                unit_choice.grid(row = counter_line, column = 5, sticky = "e", padx = 20)
                units.append(unit_choice)

                new_ing.append(ing)
                counter_line += 1
        
        data_frame.grid_columnconfigure(6, weight = 1)
        data_frame.pack(side = "top", fill = "both", expand = 1, anchor = "center")

        buttons_frame = tk.Frame(self, bg = "#2a9d8f")
        buttons_frame.grid_rowconfigure(0, weight = 1)
        buttons_frame.grid_columnconfigure(0, weight = 1)

        prev_button = tk.Button(buttons_frame, text = "Avant", font = 'arial 20 bold', bg = '#8A7E72', fg = '#5A2328', width = 12)
        buttons_frame.grid_columnconfigure(2, weight = 1)
        
        if len(ingredients) != len(species):
            prev_button.grid(row = 1, column = 1, pady = 10, sticky = "w")

        prev_button.bind('<Button-1>', lambda x: controller.show_frame(MissingSpeciesPage))

        finish_button = tk.Button(buttons_frame, text = "Terminer", font = 'arial 20 bold', bg = '#8A7E72', fg = '#5A2328', width = 12)
        finish_button.grid(row = 1, column = 3, pady = 10, sticky = "w")
        finish_button.bind('<Button-1>', lambda x: results_window_from_missing_window(self, ingredients, species, url_recipe, window, dict_nutrition, dry_matter_dico, quantities, units, new_ing))
        buttons_frame.grid_columnconfigure(4, weight = 1)


        buttons_frame.pack(side = "top", fill = "x", expand = 1, anchor = "center")


class Results:
    '''
    Creation de la fenetre pour les résultats.
    '''

    def __init__(self, ingredients, species, results_window, url_recipe, dict_nutrition, dry_matter_dico):

    # window setting 
        results_window.title("Résultats")
        results_window.geometry("1800x800")
        results_window.minsize(1080, 720)
        results_window.config(background = "#C8BFC7")

    # Main canvas
        top_frame = tk.Frame(results_window)
        top_frame.pack(fill = "both", expand = 1, anchor = "center")
        main_canvas = tk.Canvas(top_frame, bg = "#C8BFC7")
        main_canvas.pack(side = "left", fill = "both", expand = 1)
        y_scrollbar = ttk.Scrollbar(top_frame, orient = "vertical", command = main_canvas.yview)
        y_scrollbar.pack(side = "right", fill = "y", expand = 0)
        main_frame = tk.Frame(main_canvas, bg = "#C8BFC7")


    # structure of the main frame
    # - info frame
    # - table frame
    # - buttons frame
    # - results frame

        info_frame = tk.Frame(main_frame, bg = "#C8BFC7")

    # recipe's name 
        name_recipe = get_ing.get_title(url_recipe)

        recipe = tk.Label(info_frame, text = name_recipe, font = ("Open Sans", 22, "bold"), bg = '#C8BFC7', fg = "#000000", justify = "center")
        recipe.pack(side = "top", expand = 1, anchor = "center", pady = 20)


    # missing species
        missing_species_lb_frame = tk.Frame(info_frame, bg = "#C8BFC7")
        
        found_species = tk.Label(missing_species_lb_frame, text = str(len(species)), font = ("Open Sans", 18, "bold"), bg = "#C8BFC7", fg = "#000000")
        found_species.grid(row = 0, column = 0, padx = 2)
        missing_species_lb_frame.grid_columnconfigure(1, weight = 1)
        
        string1_lb = tk.Label(missing_species_lb_frame, text = "espèces ont été trouvé pour les", font = ("Open Sans", 18), bg = "#C8BFC7", fg = "#8A7E72")
        string1_lb.grid(row = 0, column = 2)
        missing_species_lb_frame.grid_columnconfigure(3, weight = 1)

        nb_ing_lb = tk.Label(missing_species_lb_frame, text = str(len(ingredients)), font = ("Open Sans", 18, "bold"), bg = "#C8BFC7", fg = "#000000")
        nb_ing_lb.grid(row = 0, column = 4, padx = 2)
        missing_species_lb_frame.grid_columnconfigure(5, weight = 1)

        string2_lb = tk.Label(missing_species_lb_frame, text = "ingrédients.",  font = ("Open Sans", 18), bg = "#C8BFC7", fg = "#8A7E72")
        string2_lb.grid(row = 0, column = 6)

        missing_species_lb_frame.pack(side = "top", expand = 1, anchor = "center", pady = 10)
        # string1="{} espèces ont été trouvé pour les {} ingrédients.".format(len(species), len(ingredients))
        # missing_species_label = tk.Label(info_frame, text = string1, font = ("Open Sans", 18), bg = '#C8BFC7', fg = "#8A7E72")
        # missing_species_label.pack(side = "top", fill = "x", expand = 1, anchor = "center")

        missing_sp_list = missing_species(ingredients, species)
        if not missing_sp_list[1]:
            missing_species2 = tk.Label(info_frame, text = "Les ingrédients pour lesquels l’espèce manque:", \
                font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
            missing_species2.pack(side = "top", fill = "x", expand = 1, anchor = "center")

            for add, sp in enumerate(missing_sp_list[0]):
                # save_row += add
                missing = tk.Label(info_frame, text = "\t"+sp, font = 'Arial 18', bg = '#C8BFC7', fg = "#000000")
                missing.pack(side = "top", fill = "x", expand = 1, anchor = "center")
        else:
            not_missing = tk.Label(info_frame, text = "Aucune espèce manque", font = 'Arial 18', bg = '#C8BFC7', \
            fg = "#000000").pack(side = "top", fill = "x", expand = 1, anchor = "center")

    # missing ingredients in nutritional db
        missing_ing_list = missing_nutrition(ingredients, dict_nutrition)
        string2="{}/{} ingrédients ont été trouvé dans la table Ciqual (base de données).".format(str(len(ingredients) \
            - len(missing_ing_list[0])),len(ingredients))
        missing_ing1 = tk.Label(info_frame, text = string2, font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
        missing_ing1.pack(side = "top", fill = "x", expand = 1, anchor = "center")

        if not missing_ing_list[1]: 
            missing_ing2 = tk.Label(info_frame, text = "Ingrédients pour lesquels aucune information a été trouvé:", \
                font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#8A7E72")
            missing_ing2.pack(side = "top", fill = "x", expand = 1, anchor = "center")

            for add1, ing in enumerate(missing_ing_list[0]):
                missing1 = tk.Label(info_frame, text = "\t"+ing, font = 'Arial 18', bg = '#C8BFC7', fg = "#000000")
                missing1.pack(side = "top", fill = "x", expand = 1, anchor = "center")

        info_frame.pack(side = "top", fill = "x")

        table_frame = tk.Frame(main_frame)
    # table
        dict_row = table_row(ingredients, species, dict_nutrition, dry_matter_dico)
        list_column = ["Ingrédient", "Espèce", "Quantité", "Qté de matière\n sèche (g)", "Eau (%)", \
            "Glucides (%)", "Lipides (%)", "Protéines (%)"]

        table_frame.grid_columnconfigure(0, weight = 1)
        save_row = 1

        for i in range(len(list_column)):
            if i == 2:
                table_header = tk.Label(table_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = "center", relief = "groove", width = 14, height = 3)
            elif i == 3:
                table_header = tk.Label(table_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = "center", relief = "groove", width = 16, height = 3)
            elif i == 4:
                table_header = tk.Label(table_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = "center", relief = "groove", width = 14, height = 3)
            elif i == 5:
                table_header = tk.Label(table_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = "center", relief = "groove", width = 14, height = 3)
            elif i == 6:
                table_header = tk.Label(table_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = "center", relief = "groove", width = 13, height = 3)
            else:
                table_header = tk.Label(table_frame, text = list_column[i], font = "Arial 14", bg = '#C8BFC7', \
                fg = "#090302", justify = "center", relief = "groove", width = 18, height = 3) 

            table_header.grid(row = save_row, column = 1+i, sticky = "nsew")

        for j in dict_row.keys():
            line = dict_row[j]
            save_row += 1
            for ind, k in enumerate(line):
                if ind == 2:
                    table_cell = tk.Label(table_frame, text = k[1]+" "+k[2][1], font = "Arial 14", bg = '#C8BFC7', \
                    fg = "#000000", justify = "center", relief = "groove", width = 14, wraplength = 300, height = 2)
                elif ind == 3:
                    table_cell = tk.Label(table_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = "center", relief = "groove", width = 16, wraplength = 300, height = 2)
                elif ind == 4:
                    table_cell = tk.Label(table_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = "center", relief = "groove", width = 14, wraplength = 300, height = 2)
                elif ind == 5:
                    table_cell = tk.Label(table_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = "center", relief = "groove", width = 14, wraplength = 300, height = 2)
                elif ind == 6:
                    table_cell = tk.Label(table_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = "center", relief = "groove", width = 13, wraplength = 300, height = 2)
                else:
                    table_cell = tk.Label(table_frame, text = k, font = "Arial 14", bg = '#C8BFC7', fg = "#000000", \
                    justify = "center", relief = "groove", width = 18, wraplength = 300, height = 2)
                table_cell.grid(row = save_row, column = 1 + ind, sticky = "nsew")

        save_row += 2
        table_frame.grid_columnconfigure(ind + 2, weight = 1)


        table_frame.pack(side = "top", fill = "both", anchor = "center", padx = 30)

    # buttons
        buttons_frame = tk.Frame(main_frame, bg = "#C8BFC7")

        def enter_download(label_photo_info):
            label_photo_info.config(text = 'Télécharger le tableau au format tsv')
        
        
        def leave_download(label_photo_info):
            label_photo_info.config(text = "")


        photo = tk.PhotoImage(file = r"assets/download_arrow.png")
        sub_photo = photo.subsample(7, 7)
        download = tk.Button(buttons_frame, image = sub_photo,  bg = '#8A7E72', width = 40, height = 40)# \
        # command = self.download_button)
        download.bind("<Button-1>", lambda x: download_button(self, results_window, ingredients, species, dry_matter_dico, dict_nutrition))
        download.image = sub_photo
        label_photo_info = tk.Label(buttons_frame, text = "", bg = '#C8BFC7', fg = "#8A7E72")
        label_photo_info.pack(side = "left")
        download.pack(side = "left")
        download.bind('<Enter>', lambda x: enter_download(label_photo_info))
        download.bind('<Leave>', lambda x: leave_download(label_photo_info))


        def get_lifemap (species):
            get_lifeMap_subTree.get_subTree(species)
            logger.info("Opening LifeMap page")
        lifemap = tk.Button(buttons_frame, text = "LifeMap Tree", font = "arial 20 bold", bg = '#8A7E72', \
        fg = "#5A2328", width = 12)
        lifemap.pack(side = "left")
        lifemap.bind('<Button-1>', lambda x: get_lifemap(species))
        
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


        ete = tk.Button(buttons_frame, text = "Ete Sub-tree", font = "arial 20 bold", bg = '#8A7E72', \
        fg = "#5A2328", width = 12)
        ete.pack(side = "left")
        ete.bind('<Button-1>', lambda x: get_ete(tree_file))


        def get_newick(tree):
            pyperclip.copy(tree)
            logger.info("The user has click the newick's button")

        newick = tk.Button(buttons_frame, text = "Newick Tree", font = "arial 20 bold", bg = '#8A7E72', fg = "#5A2328", width = 12)
        newick.pack(side = "left")
        newick.bind('<Button-1>', lambda x: get_newick(tree_file))


        label_info = tk.Label(buttons_frame, text = "", bg = '#C8BFC7', fg = "#8A7E72", width = 40)
        label_info.pack(side = "left")
        newick_info = tk.Button(buttons_frame, text = "?", font = "arial 20 bold", bg = '#8A7E72', \
        fg = "#5A2328", width = 2)
        newick_info.pack(side = "left")
        newick_info.bind('<Enter>', lambda x: enter_button(label_info, 'Le bouton "Newick Tree" \npermet de recopier le sous-arbre \nde newick dans le clipboard'))
        newick_info.bind('<Leave>', lambda x: leave_button(label_info))

        buttons_frame.pack(side = "top", fill = "both", anchor = "center")

    # Results

        results_frame = tk.Frame(main_frame, bg = "#C8BFC7")

    # Phylogenetic diversity
        pd_frame = tk.Frame(results_frame, bg = "#C8BFC7")

        pd = get_dp.phylogenetic_diversity(tree, species)

        pd_info_label = tk.Label(pd_frame, text = "Diversité phylogénétique (MPD, Webb 2002):", \
            font = 'Arial 14 bold', bg = '#C8BFC7', fg = "#8A7E72", justify = "center")
        pd_info_label.pack(side = "top")

        dp_label = tk.Label(pd_frame, text = pd, font = 'Arial 18 bold', bg = '#C8BFC7', \
        fg = "#090302", justify = "center", relief = "raised", width = 7, height = 3)
        dp_label.pack(side = "top")

        pd_frame.grid(row = 0, column = 0, padx = 20, pady = 20)

    # Weighted phylogenetic diversity
        wpd_frame = tk.Frame(results_frame, bg = "#C8BFC7")
        
        dict_sp_drym = {}
        bool_var = True
        for ing in species.keys():
            if ing in dry_matter_dico.keys() and dry_matter_dico[ing] != "-":
                dict_sp_drym[species[ing]] = dry_matter_dico[ing]
            else:
                bool_var = False
                break
        
        if bool_var is True:
            wpd = get_dp.weighted_phylogenetic_diversity(tree, species, dict_sp_drym)
            shannon = get_dp.shannon(species, dict_sp_drym)
            simpson = get_dp.simpson(species, dict_sp_drym)
        else:
            wpd = "NA"
            shannon = "NA"
            simpson = "NA"
        
        wpd_info_label = tk.Label(wpd_frame, text = "Diversité phylogénétique pondérée:", font = 'Arial 14 bold', \
            bg = '#C8BFC7', fg = "#8A7E72", justify = "center")
        wpd_info_label.pack(side = "top")

        wpd_label = tk.Label(wpd_frame, text = wpd,  font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#090302", \
        justify = "center", relief = "raised", width = 7, height = 3)
        wpd_label.pack(side = "top")

        wpd_frame.grid(row = 0, column = 1)

    # Shannon's index
        shannon_frame = tk.Frame(results_frame, bg = "#C8BFC7")
        shannon_info_label = tk.Label(shannon_frame, text = "Indice de Shannon:", font = 'Arial 14 bold', \
            bg = '#C8BFC7', fg = "#8A7E72", justify = "center")
        shannon_info_label.pack(side = "top")
        shannon_label = tk.Label(shannon_frame, text = shannon, font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#090302", \
        justify = "center", relief = "raised", width = 7, height = 3)
        shannon_label.pack(side = "bottom")
        shannon_frame.grid(row = 1, column = 0, padx = 20, pady = 20)

    # Simpson's index
        simpson_frame = tk.Frame(results_frame, bg = "#C8BFC7")
        simpson_info_label = tk.Label(simpson_frame, text = "Indice de Simpson:", font = 'Arial 14 bold', \
            bg = '#C8BFC7', fg = "#8A7E72", justify = "center")
        simpson_info_label.pack(side = "top")
        simpson_label = tk.Label(simpson_frame, text = simpson, font = 'Arial 18 bold', bg = '#C8BFC7', fg = "#090302", \
        justify = "center", relief = "raised", width = 7, height = 3)
        simpson_label.pack(side = "bottom")
        simpson_frame.grid(row = 1, column = 1, padx = 20, pady = 20) 


        results_frame.pack(side = "bottom", pady = 20)

        main_frame.configure(width = main_canvas.winfo_reqwidth())
        main_frame.pack(side = "right", fill = "both", expand = 1, anchor = "center")
        main_canvas.update_idletasks()       
        main_canvas.configure(yscrollcommand = y_scrollbar.set, highlightthickness = 0)

    # Mousewheel
        main_frame.bind('<Configure>', lambda event: main_canvas.configure(scrollregion = main_canvas.bbox("all")))
        main_frame.bind_all('<Button-4>', lambda event: main_canvas.yview('scroll', -1, 'units'))
        main_frame.bind_all('<Button-5>', lambda event: main_canvas.yview('scroll', 1, 'units'))
        main_frame.bind_all('<MouseWheel>', lambda event: main_canvas.yview('scroll', 1, 'units'))
        main_frame.bind_all('<MouseWheel>', lambda event: main_canvas.yview('scroll', -1, 'units'))

    # create window
        main_canvas.create_window((main_canvas.winfo_reqwidth()/2, 0), window = main_frame, anchor = "nw")
        


        def download_button(self, results_window, ingredients, species, dry_matter_dico, dict_nutrition):
            '''
            Ouvre la fenetre pour nommer le fichier qui aura le tableau au format tsv.
            '''
            try:
                self.download = tk.Toplevel(results_window)
                self.app = Download(self.download, ingredients, species, dry_matter_dico, dict_nutrition)
                logger.info("The user has click the download button for the tsv table")
            except Exception:
                logger.exception("Error in opening download window")


class Download:
    '''
    Creation de la fenetre qui permet de rentrer le nom du fichier dans lequel on souhaite telecharger le tableau au format csv ou tsv.
    '''
    def __init__(self, download_window, ingredients, species, dry_matter_dico, dict_nutrition):
        self.download_window = download_window
        
    # window setting 
        download_window.title("Enregistrement")
        download_window.geometry("700x200")
        download_window.minsize(800, 200)
        download_window.config(background = "#C8BFC7")
        download_window.grid_rowconfigure(0, weight = 1)

    # introducing label
        intro_label = tk.Label(self.download_window, text = "Le fichier sera enregistré dans le répertoire contenant le programme au format tsv.\nChoississez le nom du fichier:", \
                font = "arial 11",foreground = "black", bg = "#C8BFC7", justify = "center")
        intro_label.grid(row = 1, column = 1)
    # file name entry
        file_name = tk.Entry(self.download_window, font = "arial 11", width = 40)
        file_name.grid(row = 2, column = 1)

        download_window.grid_rowconfigure(3, weight = 1)

    # confirm button

        def action (file_name, ingredients, species, dry_matter_dico, dict_nutrition):
            file_name = file_name.get()
            if not file_name.endswith(".tsv"):
                file_name += ".tsv"
            logger.info("TSV table saved with the filename: " + file_name)
            ing_properties.write_tsv(file_name, ingredients, species, dry_matter_dico, dict_nutrition)
            self.download_window.destroy()
        confirm_button = tk.Button(self.download_window, text = "Enregistrer", font  = "arial 11", width = 10)
        confirm_button.grid(row = 4, column = 1)
        confirm_button.bind("<Button-1>", lambda x: action(file_name, ingredients, species, dry_matter_dico, dict_nutrition))

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
    root = MainWindow()
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
