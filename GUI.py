#  -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk
from PIL import ImageTk, Image
from urllib.parse import urlparse
import webbrowser
from lib import get_lifeMap_subTree, get_ing, ing_to_esp, get_dp, ing_properties
import pyperclip
from ete3 import NCBITaxa
import os, sys, inspect
import logging

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
        self.minsize(800,470)
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


    # submit buttons
        submit_buttons_frame = tk.Frame(self.main_frame, bg = "#2a9d8f", height = 50)
        
    # mono-recipe
        recipes_dict = {}
        def mono_recipe_func():
            recipes_dict = {}
            url = self.url_entry.get()
            recipes_dict[url] = []
            name_recipe = get_ing.get_title(url).replace("/", "")
            filename = "_" + name_recipe + ".tsv"
            filename =filename.replace(" ", "_")
            self.url_process(recipes_dict, filename)

            
        submit = ctk.CTkButton(master = submit_buttons_frame, text = 'Entrer', bg_color = "#2a9d8f", \
        fg_color = "#f0efeb", command = mono_recipe_func, width = 200, height = 44, \
        corner_radius = 20, text_font = ("Open Sans", 20, "bold"), hover_color = "#B7B7A4", \
        text_color = "#5aa786")
        submit.pack(side = "left", expand = 1, anchor = "center", padx = 10) 

    # multi-recipe
        def multi_recipe_func():
            file_name = filedialog.askopenfilename(parent = self, title = "multi-recette")
            recipes_dict = {}
            
            if file_name != ():
                # parse list of URLs
                with open(file_name, "r", encoding="utf-8") as f:
                    list_url = f.readlines()
                    for url in list_url:
                        recipes_dict[url.replace("\n", "")] = []
            
                if "." in file_name:
                    file_name = file_name[:file_name.rfind(".")]
                if "/" in file_name:
                    file_name = file_name[file_name.rfind("/"):]
                filename = file_name.replace("/", "_").replace(" ", "_")
                filename = "_" + filename + ".tsv"
                self.url_process(recipes_dict, filename)


        multirecipe_button = ctk.CTkButton(master = submit_buttons_frame, text = "+", bg_color = "#2a9d8f", \
        fg_color = "#f0efeb", command = multi_recipe_func, width = 44, height = 44, \
        corner_radius = 25, text_font = ("Open Sans", 20, "bold"), hover_color = "#B7B7A4", \
        text_color = "#5aa786")
        multirecipe_button.pack(side = "left", expand = 1, anchor = "e", padx = 10)

        multi_label = tk.Label(submit_buttons_frame, text = "multi-recette", font = ("Open Sans", 14, "bold"), \
            bg = "#2a9d8f", fg = "#f0efeb")
        multi_label.pack(side = "right", anchor = "w")
        
        submit_buttons_frame.pack(side = "top", anchor = "center", pady = 20)


        def open_tsv():
            file_name = filedialog.askopenfilename(parent = self, title = "open tsv file")
            recipes_dict = {}
            
            if file_name != ():
                # parse the TSV file; TODO: control point
                with open(file_name, "r", encoding="utf-8") as f:
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
                filename = file_name.replace("/", "_").replace(" ", "_")
                filename = "_" + filename + ".tsv"
                self.url_process(recipes_dict, filename)

        tsv_frame = tk.Frame(self.main_frame, bg = "#2a9d8f", height = 50)
        tsv_button = ctk.CTkButton(master = tsv_frame, text = "tsv", bg_color = "#2a9d8f", \
        fg_color = "#f0efeb", command = open_tsv, width = 80, height = 44, \
        corner_radius = 25, text_font = ("Open Sans", 20, "bold"), hover_color = "#B7B7A4", \
        text_color = "#5aa786")
        tsv_label = tk.Label(tsv_frame, text = "Entrer une recette au format .tsv", font = ("Open Sans", 14, "bold"), bg = "#2a9d8f", fg = "#f0efeb")
        tsv_button.pack(side = "left", expand = 1, anchor = "e", padx = 10)
        tsv_label.pack(side = "right", expand = 1, anchor = "e", padx = 10)
        tsv_frame.pack(side = "bottom", anchor = "center", pady = 10)

    #  utility buttons
        bottom_frame = tk.Frame(self, bg = "#2a9d8f")
        button_frame = ctk.CTkFrame(master = bottom_frame, bg = "#2a9d8f", fg_color = "#2a9d8f", height = 50, width = 800)
        info_label = tk.Label(button_frame, text = "", bg = "#e4e4dd", fg = "#000000")


        # gitlab button     
        def open_gitlab():
            webbrowser.open("https://gitlab.com/TommasoBarberis/diversite-phylogenetique-de-l-assiette-au-jardin", new = 2)

        def info_label_enter(evt, text):
            def after_func():
                info_label.configure(text = text)
                info_label.place_configure(x = evt.x + 15, y = evt.y + bottom_frame.winfo_reqheight() - 25)
                info_label.lift()
        
            info_label.after(500, func = after_func)


        def info_label_leave(evt):
            def after_func():
                info_label.place_forget()

            info_label.after(500, func = after_func)


        gitlab_icon = tk.PhotoImage(file = r"assets/gitlab.png").subsample(5, 5)
        gitlab_button = ctk.CTkButton(master =button_frame, bg_color = "#2a9d8f", fg_color = "#f0efeb", \
            text= "", width = 50, height = 50, corner_radius = 5, \
            image = gitlab_icon, hover_color = "#B7B7A4", command = open_gitlab)
        gitlab_button.pack(side = "left", expand = 0, anchor = "sw", padx = 15, pady = 10) 
        gitlab_button.bind("<Enter>", lambda x: info_label_enter(x, "Gitlab - Diversité phylogénétique: de l'assiette au jardin"))
        gitlab_button.bind("<Leave>", info_label_leave)

        # ucbl button
        def open_ucbl():
            webbrowser.open("https://www.univ-lyon1.fr/", new = 2)

        ucbl_icon = tk.PhotoImage(file = r"assets/ucbl.png").subsample(5, 5)
        ucbl_button = ctk.CTkButton(master =button_frame, bg_color = "#2a9d8f", fg_color = "#f0efeb", \
            text= "", width = 50, height = 50, corner_radius = 5, \
            image = ucbl_icon, hover_color = "#B7B7A4", command = open_ucbl)
        ucbl_button.pack(side = "left", expand = 0, anchor = "sw", padx = 15, pady = 10)
        ucbl_button.bind("<Enter>", lambda x: info_label_enter(x, "Université Claude Bernard Lyon 1"))
        ucbl_button.bind("<Leave>", info_label_leave)


        # marmitton button
        def open_marmiton():
            webbrowser.open("https://www.marmiton.org/", new = 2)

        marmiton_icon = tk.PhotoImage(file = r"assets/marmiton.png").subsample(7, 7)
        marmiton_button = ctk.CTkButton(master =button_frame, bg_color = "#2a9d8f", fg_color = "#f0efeb", \
            text= "", width = 50, height = 50, corner_radius = 5, \
            image = marmiton_icon, hover_color = "#B7B7A4", command = open_marmiton)
        marmiton_button.pack(side = "left", expand = 0, anchor = "sw", padx = 15, pady = 10)
        marmiton_button.bind("<Enter>", lambda x: info_label_enter(x, "Marmiton - site de cuisine"))
        marmiton_button.bind("<Leave>", info_label_leave)

    # logo
        self.logo = Image.open(r"assets/logo.png")
        self.logo = self.logo.resize((170, 170), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(bottom_frame, image = self.logo, bg = "#2a9d8f")

        self.main_frame.pack(side = "top", fill = "both", expand = 1, anchor = "center")
        bottom_frame.pack(side = "bottom", fill = "both", expand = 1)
        button_frame.pack(side = "left", fill = "both", expand = 1, anchor = "s")
        self.logo_label.pack(side = "right", padx = 20, anchor = "n")


    def url_process(self, recipes_dict, filename):
        '''
        pour tester si l'url est valide, si c'est le cas il ouvre une nouvelle fenêtre pour 
        demander les informations manquantes ou sinon directement pour afficher les résultats,
        autrement il affiche une fenêtre d'erreur.
        '''
        
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        ingredients = None
        counter = 1

        for url in recipes_dict:
            if recipes_dict[url] != []:
                try:
                    ingredients = recipes_dict[url][0]
                except:
                    pass

                recipes_dict[url] = []
            else:
                try:
                    ingredients = get_ing.process(url)
            
                except Exception:
                    logger.exception("{} url is wrong".format(url))

                    if calframe[1][3] == "mono_recipe_func":
                        self.error_window("L'URL saisi est incorrect.")
                    elif calframe[1][3] == "multi_recipe_func":
                        self.error_window("L'URL à la ligne numéro {} est incorrect.".format(counter))
                        break
                
                counter += 1
                logger.info("Processing: " + url)

                
                try:
                    assert ingredients is not None
                except AssertionError as err:
                    logger.exception(err)
                    logger.error("Parse error")
                    sys.exit()
                    self.destroy()

            species = ing_to_esp.recherche_globale(ingredients)
            dict_nutrition = ing_properties.get_dict_nut(ingredients)
            dry_matter_dico = ing_properties.dry_matter_dict_update(ingredients, dict_nutrition)

            recipes_dict[url] = [ingredients, species, dict_nutrition, dry_matter_dico]
            logger.info("URL processed, getting ingredient, species, nutrition data and dry matter information")

        var = True  # to check if there are some missing info
        for recipe in recipes_dict:
            ing = recipes_dict[recipe][0]
            sp = recipes_dict[recipe][1]
            nut = recipes_dict[recipe][2]
            drym = recipes_dict[recipe][3]
            
            if len(ing) != len(sp):
                var = False
                sp = [sp, False]
            if "NA" in drym.values():
                var = False
                drym = [drym, False]

            recipes_dict[recipe] = [ing, sp, nut, drym]

        if var:
            try:
                self.results_window(ingredients, species, url, dict_nutrition, dry_matter_dico)
                logger.info("Open result window")
                self.iconify()
            except Exception:
                logger.exception("Error in 'result' window opening")
        
        else:
            try:
                self.missing_info_window(recipes_dict, filename)
                logger.info("Open missing information window")
                self.iconify()
            except:
                logger.exception("Error in 'missing information' window opening")

        return None   


    def error_window(self, label_text):
        '''
        Ouvre la fenetre d'erreur.
        '''
        try:
            logger.info("Open error window for incorrect url")
            self.error = tk.Toplevel(self)
            self.app = ErrorWin(self.error, label_text)
        except Exception:
            logger.exception("Error in 'error' window opening")


    def results_window(self, ingredients, species, dict_nutrition, dry_matter_dico): 
        '''
        Ouvre la fenetre des resultats.
        '''  

        self.results = tk.Toplevel(self)
        self.app = Results(ingredients, species, self.results, self.url_entry.get(), dict_nutrition, dry_matter_dico)

    def missing_info_window(self, recipes_dict, filename):
        '''
        Ouvre la fenetre pour rajouter les informations manquantes
        '''

        self.missing = tk.Toplevel(self)
        self.app = MissingPage(self.missing, recipes_dict, filename)



class ErrorWin:
    '''
    Creation de la fenetre pour le message d'erreur.
    '''


    def __init__(self, error_window, label_text):
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
        error_message = tk.Label(main_frame, text = label_text, \
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


class MissingPage:
    '''
    Creation de la fenetre pour recuperer les informations manquantes
    '''

    def __init__(self, missing_window, recipes_dict, filename):
        # self.missing_window = missing_window

    # window setting 
        missing_window.title("Informations manquantes")
        w = 1200
        h = 740
        x = (missing_window.winfo_screenwidth() - w) / 2
        y = (missing_window.winfo_screenheight() - h) / 2
        missing_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        missing_window.minsize(800,400)
        missing_window.config(background = "#2a9d8f")

        list_recipe = [] # list of recipes that miss some info
        for recipe in recipes_dict:
            if isinstance(recipes_dict[recipe][1], list) or isinstance(recipes_dict[recipe][3], list):
                list_recipe.append(recipe)
        
        for counter, recipe in enumerate(list_recipe):
            var = "central"
            if counter == 0:
                var = "left" # in order to not show previous button in the first frame
            elif counter == (len(list_recipe) - 1):
                var = "right" # in order to not show continue button in the last frame
            list_recipe[counter] = [recipe, var]
        if len(list_recipe) == 1:
            list_recipe = [[list_recipe[0][0], "single"]]

        main_frame = tk.Frame(missing_window, bg = "#2a9d8f")
        main_frame.pack(fill = "both", expand = 1, anchor = "center")
        self.frames = {}

        main_frame.grid_rowconfigure(0, weight = 1)
        main_frame.grid_columnconfigure(0, weight = 1)

        for recipe in list_recipe:
            frame = containerFrame(main_frame, self, missing_window, recipe, recipes_dict, list_recipe, filename)
            self.frames[recipe[0]] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_deeper_frames(list_recipe[0][0])
    
    def show_deeper_frames(self, frame_name):
        self.frames[frame_name].tkraise()
        logger.info("Show {} frame".format(frame_name))

   
def results_window_from_missing_window(self, window, recipes_dict, filename): 
    '''
    Ouvre la fenetre des resultats.
    '''  
    for recipe in recipes_dict:
        ingredients = recipes_dict[recipe][0]

        species = recipes_dict[recipe][1]
        if isinstance(species, list):
            species = species[0]

        drym = recipes_dict[recipe][3]
        if isinstance(drym, list):
            drym = drym[0]

        for ing in ingredients:
            if ing not in species.keys():
                species[ing] = "NA"



        recipes_dict[recipe] = [recipes_dict[recipe][0], species, recipes_dict[recipe][2], drym]
        
    header = ["recipe_name", "ingredients", "quantity", "unit", "url"]
    with open(filename, "w") as bkp:
        header_line = ""
        for column in header:
            header_line += column + "\t"
        if header_line.endswith("\t"):
            header_line = header_line[:-1]
        bkp.write(header_line + "\n")

        for recipe in recipes_dict:
            recipe_name = get_ing.get_title(recipe)
            ingredients = recipes_dict[recipe][0]
            for ing in ingredients:
                qty = ingredients[ing][1]
                unit = ingredients[ing][2][0]
                line = recipe_name + "\t" + ing + "\t" + qty + "\t" + unit + "\t" + recipe
                bkp.write(line + "\n")

    self.results = tk.Toplevel(self)
    self.app = Results(self.results, recipes_dict)
    window.withdraw()


class containerFrame(tk.Frame):
    def __init__(self, parent, controller, window, recipe, recipes_dict, list_recipe, filename):
        tk.Frame.__init__(self, parent)
        self.list_recipe = list_recipe
        self.controller = controller

        main_frame = tk.Frame(self, bg = "#2a9d8f")
        main_frame.pack(fill = "both", expand = 1, anchor = "center")
        
        main_frame.grid_rowconfigure(0, weight = 1)
        main_frame.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for F in (MissingSpeciesPage, MissingQuantitiesPage): 
            frame = F(main_frame, self, window, recipe, recipes_dict, filename)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        sp = recipes_dict[recipe[0]][1] 

        if isinstance(sp, list): # if some species are missed
            self.show_frame(MissingSpeciesPage)
        else:
            self.show_frame(MissingQuantitiesPage)


    def change_container(self, recipe, caller, recipes_dict, window):
        counter = 0
        if caller == "next_button":
            index = self.list_recipe.index(recipe) + 1 # swtich to the following recipe

            url = self.list_recipe[index][0]
            ing_temp = recipes_dict[url][0]
            try:
                species_temp = recipes_dict[url][1][0]
            except:
                species_temp = recipes_dict[url][1]
            counter = len(ing_temp) - len(species_temp)

        elif caller == "prev_button":
            index = self.list_recipe.index(recipe) - 1 # swtich to the previous recipe

            url = self.list_recipe[index][0]
            try:
                drym_temp = recipes_dict[url][3][0]
            except:
                drym_temp = recipes_dict[url][3]
            for ing in drym_temp:
                if drym_temp[ing] == "NA":
                    counter += 1

        w = 1000
        h = 400 + (counter * 30)
        x = (window.winfo_screenwidth() - w) / 2
        y = (window.winfo_screenheight() - h) / 2 - 100
        window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.controller.show_deeper_frames(self.list_recipe[index][0])


    def show_frame(self, frame_name):
        self.frames[frame_name].tkraise()
        logger.info("Show {} frame".format(frame_name.__name__))
    

class MissingSpeciesPage(tk.Frame):

    def __init__(self, parent, controller, window, recipe, recipes_dict, filename):
        tk.Frame.__init__(self, parent)
        self.config(bg = "#2a9d8f")

    # frame for title and instruction     
        top_frame = tk.Frame(self, bg = "#2a9d8f")
        title_label = tk.Label(top_frame, text = get_ing.get_title(recipe[0]), font = ("Open Sans", 20, "bold"), \
            bg = '#2a9d8f', fg = "#f0efeb", wraplength = 900)
        title_label.pack(expand = 1, anchor = "center", pady = 15)
        
        instruction_label = tk.Label(top_frame, \
            text = "Si c'est possible, renseigner les \nespèces pour les ingrédients suivants:", \
            font = ("Open Sans", 18), bg = '#2a9d8f', fg = "#f0efeb")
        instruction_label.pack(expand = 1, anchor = "center")


    # frame for data insertion
        data_frame = tk.Frame(self, bg = "#2a9d8f")
        data_frame.grid_columnconfigure(0, weight = 1)
        data_frame.grid_rowconfigure(0, weight = 1)
        counter_line = 3
        
        entries = []
        ingredients = recipes_dict[recipe[0]][0]

        try:
            species = recipes_dict[recipe[0]][1][0]
        except:
            species = recipes_dict[recipe[0]][1]

        for ing in ingredients:
            if ing not in species:
                ing_cell = tk.Label(data_frame, text = ing, font = ("Open Sans", 16, "bold"), bg = '#2a9d8f', \
                fg = "#f0efeb")
                ing_cell.grid(row = counter_line, column = 1, sticky = "e", padx = 20)

                sp_entry = ctk.CTkEntry(data_frame, font = ("Arial", 10), width = 500, corner_radius = 10)
                sp_entry.grid(row = counter_line, column = 3, sticky = "w")

                not_valid_label = tk.Label(data_frame, text = "", font = ("Open Sans", 10, "bold"), bg = '#2a9d8f', fg = "#f0efeb", width = 30)
                not_valid_label.grid(row = counter_line, column = 5, sticky = "nsew")

                entries.append((ing, sp_entry, not_valid_label))

                counter_line += 1

        data_frame.grid_rowconfigure(counter_line + 1, weight = 1)


    # frame for the test button
        test_button_frame = ctk.CTkFrame(master = self, bg = "#2a9d8f", fg_color = "#2a9d8f")

        def test_button_func():
            test_species(entries)

        test_button = ctk.CTkButton(master = test_button_frame, text = "Test", text_font = ("Open Sans", 20, "bold"), \
        bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
        height = 40, corner_radius = 20, command = test_button_func)    
        test_button.pack(side = "top", anchor = "n")
 

        def test_species(entries):
            '''
            Permet de tester si les espèces rentrées par l'utilisateur sont des noms taxonomiques valides
            '''

            for entry in entries:
                ing = entry[0]
                new_specie = entry[1].get()
                err_label = entry[2]
                if entry != "":
                    logger.debug("The user has enter '{}' for the ingredient '{}'".format(new_specie, ing))
                sp = get_lifeMap_subTree.get_taxid({entry: new_specie})

                if sp != []:
                    species[ing] = new_specie
                    err_label.config(text = "")

                    with open("data/filtered_scientific_name_db.txt", "a", encoding="utf-8") as name_db:
                        new_line = str(new_specie) + "\t" + str(ing + "\n")
                        name_db.write(new_line)

                    with open("data/filtered_scientific_name_db.txt", "r", encoding="utf-8") as name_db:
                        lines = name_db.readlines()

                    with open("data/filtered_scientific_name_db.txt", "w", encoding="utf-8") as name_db:

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
                    err_label.config(text = "Nom taxonomique non valide")

                recipes_dict[recipe[0]] = [recipes_dict[recipe[0]][0], species, recipes_dict[recipe[0]][2], recipes_dict[recipe[0]][3]]

        
        # TODO - label that explain the button function
        # label_info = tk.Label(buttons_frame, text = "", bg = '#2a9d8f', fg = "#8A7E72", width = 50)
        # label_info.grid(row = 1, column = 3, sticky = "nsew")
        # test_button.bind('<Enter>', lambda x: enter_button(label_info, 'Permet de tester si les espèces rentrées \nsont des noms taxonomiques valides'))
        # test_button.bind('<Leave>', lambda x: leave_button(label_info))


    # frame for button in the bottom of page
        final_buttons_frame = ctk.CTkFrame(master = self, bg = "#2a9d8f", fg_color = "#2a9d8f")


        def prev_button_func():
            controller.change_container(recipe, "prev_button", recipes_dict, window)

        prev_button = ctk.CTkButton(master = final_buttons_frame, text = "Avant", text_font = ("Open Sans", 20 ,"bold"), \
            bg_color = '#2a9d8f', fg_color = '#f0efeb', width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
            height = 40, corner_radius = 20, command = prev_button_func)


        def next_button_func():
            controller.show_frame(MissingQuantitiesPage)
            counter = 0
            try:
                drym_temp = recipes_dict[recipe[0]][3][0]
            except:
                drym_temp = recipes_dict[recipe[0]][3]
            counter = 0
            for ing in drym_temp:
                if drym_temp[ing] == "NA":
                    counter += 1

            w = 1000
            h = 400 + (counter * 30)
            x = (window.winfo_screenwidth() - w) / 2
            y = (window.winfo_screenheight() - h) / 2 - 100
            window.geometry("%dx%d+%d+%d" % (w, h, x, y))

        next_button = ctk.CTkButton(master = final_buttons_frame, text = "Suivant", text_font = ("Open Sans", 20, "bold"), \
        bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
        height = 40, corner_radius = 20, command = next_button_func)

        def finish_button_func():
            results_window_from_missing_window(self, window, recipes_dict, filename)

        finish_button = ctk.CTkButton(master = final_buttons_frame, text = "Terminer", text_font = ("Open Sans", 20, "bold"), \
        bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
        height = 40, corner_radius = 20, command = finish_button_func)

        dry_matter_dico = recipes_dict[recipe[0]][3]
        var = recipe[1]

        if var == "single":
            if isinstance(dry_matter_dico, list): # it allow or not to open the "window" to modify quantities
                next_button.pack(side = "right", anchor = "se", padx = 10, pady = 10)
            else:
                finish_button.pack(side = "right", anchor = "se", padx = 10, pady = 10)
        elif var == "left":
            next_button.pack(side = "right", anchor = "se", padx = 10, pady = 10)
        elif var == "central":
            prev_button.pack(side = "left", anchor = "sw", padx = 10, pady = 10)
            next_button.pack(side = "right", anchor = "se", padx = 10, pady = 10)
        elif var == "right":
            prev_button.pack(side = "left", anchor = "sw", padx = 10, pady = 10)
            if isinstance(dry_matter_dico, list):
                next_button.pack(side = "right", anchor = "se", padx = 10, pady = 10)
            else:
                finish_button.pack(side = "right", anchor = "se", padx = 10, pady = 10)

        top_frame.pack(side = "top", fill = "x", expand = 1,  anchor = "center")
        data_frame.pack(side = "top", fill = "x", expand = 1, anchor = "center")
        test_button_frame.pack(side = "top", fill = "x", expand = 1, anchor = "n")
        final_buttons_frame.pack(side = "top", fill = "x", expand = 1, anchor = "se")


class MissingQuantitiesPage(tk.Frame):

    def __init__(self, parent, controller, window, recipe, recipes_dict, filename):
        tk.Frame.__init__(self, parent)
        self.config(bg = "#2a9d8f")

    # frame for title and instruction     
        top_frame = tk.Frame(self, bg = "#2a9d8f")
        title_label = tk.Label(top_frame, text = get_ing.get_title(recipe[0]), font = ("Open Sans", 20, "bold"), \
            bg = '#2a9d8f', fg = "#f0efeb")
        title_label.pack(expand = 1, anchor = "center", pady = 15)
        
        instruction_label = tk.Label(top_frame, \
            text = "Si c'est possible, renseigner les quantités \npour les ingrédients suivants ainsi que leurs unités de mesure:", \
            font = ("Open Sans", 18), bg = '#2a9d8f', fg = "#f0efeb")
        instruction_label.pack(expand = 1, anchor = "center")


    # frame to insert new data
        data_frame = tk.Frame(self, bg = "#2a9d8f")
        data_frame.grid_columnconfigure(0, weight = 1)
        data_frame.grid_rowconfigure(0, weight = 1)
        counter_line = 3
        
        entries = []
        ingredients = recipes_dict[recipe[0]][0]
        try:
            dry_matter_dico = recipes_dict[recipe[0]][3][0]
        except:
            dry_matter_dico = recipes_dict[recipe[0]][3]

        for ing in dry_matter_dico:
            if dry_matter_dico[ing] == "NA":
                ing_label = tk.Label(data_frame, text = ing, font = ("Open Sans", 16, "bold"), bg = '#2a9d8f', fg = "#f0efeb")
                ing_label.grid(row = counter_line, column = 1, sticky = "e", padx = 20)

                quantity_entry = ctk.CTkEntry(data_frame, font = ("Arial", 10), width = 400, corner_radius = 10)
                quantity_entry.grid(row = counter_line, column = 3, sticky = "w")

                unit_choice = ttk.Combobox(data_frame, width = 10)
                unit_choice['values'] = ('g', 'kg', 'cl', 'dl', 'l')
                unit_choice.grid(row = counter_line, column = 5, sticky = "e", padx = 20)

                err_label = tk.Label(data_frame, font = ("Open Sans", 10, "bold"), bg = '#2a9d8f', fg = "#f0efeb", \
                width = 20)
                err_label.grid(row = counter_line, column = 7, sticky = "w")

                entries.append((ing, quantity_entry, unit_choice, err_label))
                counter_line += 1
        
        data_frame.grid_columnconfigure(6, weight = 1)

    # frame to place buttons
        buttons_frame = tk.Frame(self, bg = "#2a9d8f")


        def prev_button_func():
            counter = 0 
            controller.show_frame(MissingSpeciesPage)
            try:
                spec_temp = recipes_dict[recipe[0]][1][0]
            except:
                spec_temp = recipes_dict[recipe[0]][1]
            counter = len(recipes_dict[recipe[0]][0]) - len(spec_temp)

            w = 1000
            h = 400 + (counter * 30)
            x = (window.winfo_screenwidth() - w) / 2
            y = (window.winfo_screenheight() - h) / 2 - 100
            window.geometry("%dx%d+%d+%d" % (w, h, x, y))


        prev_button = ctk.CTkButton(master = buttons_frame, text = "Avant", text_font = ("Open Sans", 20 ,"bold"), \
            bg_color = '#2a9d8f', fg_color = '#f0efeb', width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
            height = 40, corner_radius = 20, command = prev_button_func)
        

        def next_button_func():
            test_qty(self, window, recipe, recipes_dict, entries, "next_button")

        next_button = ctk.CTkButton(master = buttons_frame, text = "Suivant", text_font = ("Open Sans", 20, "bold"), \
        bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
        height = 40, corner_radius = 20, command = next_button_func)


        def end_button_func():
            test_qty(self, window, recipe, recipes_dict, entries, "end_button")

        finish_button = ctk.CTkButton(master = buttons_frame, text = "Terminer", text_font = ("Open Sans", 20 ,"bold"), \
            bg_color = '#2a9d8f', fg_color = '#f0efeb', width = 200, hover_color = "#B7B7A4", text_color = "#5aa786", \
            height = 40, corner_radius = 20, command = end_button_func)

        try:
            species = recipes_dict[recipe[0]][1][0]
        except:
            species = recipes_dict[recipe[0]][1]
        
        var = recipe[1]

        if var == "single" or var == "right":
            finish_button.pack(side = "right", anchor = "se", padx = 10, pady = 10)
        elif var == "left" or var == "central":
            next_button.pack(side = "right", anchor = "se", padx = 10, pady = 10)

        if len(ingredients) != len(species):
            prev_button.pack(side = "left", anchor = "sw", padx = 10, pady = 10)



        def test_qty(self, window, recipe, recipes_dict, entries, caller):
            
            var = True 
            ingredients = recipes_dict[recipe[0]][0] 
            dict_nutrition = recipes_dict[recipe[0]][2]
          
            for entry in entries:
                ing = entry[0]
                new_qty = entry[1].get()
                new_unit = entry[2].get()
                err_label = entry[3]

                if new_qty != "" or new_unit != "": # if any quantities or units is given, the original data are conserved
                    if new_qty.isnumeric() and new_unit in ("g", "kg", "l", "dl", "cl"):
                        ingredients[ing] = [ingredients[ing][0], new_qty, [new_unit, new_unit]]
                        recipes_dict[recipe[0]] = [ingredients, recipes_dict[recipe[0]][1],  recipes_dict[recipe[0]][2], recipes_dict[recipe[0]][3]]        
                        err_label.config(text = "")
                        logger.debug("The user add {} quantity and unit for the ingredient {}".format(str(new_qty + " " + str(new_unit)), ing))
                    elif new_qty.isnumeric() is False:
                        err_label.config(text = "Erreur dans la quantité")
                        var = False
                    elif new_unit not in ("g", "kg", "l", "dl", "cl"):
                        err_label.config(text = "Erreur dans l'unité")
                        var = False
                elif new_qty == "" and new_unit != "":
                        err_label.config(text = "Quantité manquante")
                elif new_unit == "" and new_qty != "":
                        err_label.config(text = "Unité manquante")
                else:
                    err_label.config(text = "")

            dry_matter_dico = ing_properties.dry_matter_dict_update(ingredients, dict_nutrition)     
            recipes_dict[recipe[0]] = [recipes_dict[recipe[0]][0], recipes_dict[recipe[0]][1],  recipes_dict[recipe[0]][2], dry_matter_dico]        

            if var:
                if caller == "next_button":
                    controller.change_container(recipe, "next_button", recipes_dict, window)
                elif caller == "end_button":
                    results_window_from_missing_window(self, window, recipes_dict, filename)


        top_frame.pack(side = "top", fill = "both", expand = 1, anchor = "center")
        data_frame.pack(side = "top", fill = "both", expand = 1, anchor = "center")
        buttons_frame.pack(side = "top", fill = "x", expand = 1, anchor = "se")

        w = 1000
        h = 400 + (counter_line * 20)
        x = (window.winfo_screenwidth() - w) / 2
        y = (window.winfo_screenheight() - h) / 2 - 100
        window.geometry("%dx%d+%d+%d" % (w, h, x, y))


class Results:
    '''
    Creation de la fenetre pour les résultats.
    '''

    def __init__(self, results_window, recipes_dict):

    # window setting 
        results_window.title("Résultats")
        w = 1300
        h = 800
        x = (results_window.winfo_screenwidth() - w) / 2
        y = (results_window.winfo_screenheight() - h) / 2
        results_window.geometry("%dx%d+%d+%d" % (w, h, x, y))

        results_window.minsize(1080, 720)
        results_window.config(background = "#2a9d8f")
        results_window.lift()

    # Deep level
        main_canvas = tk.Canvas(results_window, bg = "#2a9d8f")
        main_canvas.pack(side = "left", fill = "both", expand = 1, anchor = "e")
   
    # scrollbar
        y_scrollbar = ttk.Scrollbar(results_window, orient = "vertical", command = main_canvas.yview)
        y_scrollbar.pack(side = "right", fill = "y", expand = 0)
        
    # Main level
        global_frame = tk.Frame(main_canvas, bg = "#2a9d8f")

        self.tables = {} # container for results tables in order to avoid the garbage collector
        ncbi = NCBITaxa() # ncbi taxonomy to build phylogenetic trees
        titles = {} # for the listbox, in order to chose the recipe to activate buttons

        for recipe in recipes_dict:
            main_frame = tk.Frame(global_frame, bg = "#2a9d8f")

            url_recipe = recipe
            ingredients = recipes_dict[recipe][0]
            species = recipes_dict[recipe][1]
            dict_nutrition = recipes_dict[recipe][2]
            dry_matter_dico = recipes_dict[recipe][3]

        # structure of the main frame
        # - info frame (recipe title and missing species)
        # - table frame 
        # - final frame (buttons and stats)
        

            info_frame = tk.Frame(main_frame, bg = "#2a9d8f")

        # recipe's name 
            name_recipe = get_ing.get_title(url_recipe).replace("/", "")
            titles[name_recipe] = url_recipe

            recipe_label = tk.Label(info_frame, text = name_recipe, font = ("Open Sans", 25, "bold"), \
                bg = "#2a9d8f", fg = "#f0efeb", justify = "center")
            recipe_label.pack(side = "top", expand = 1, anchor = "center", pady = 20)


        # missing species
            missing_species_lb_frame = tk.Frame(info_frame, bg = "#2a9d8f")
            found = 0
            for sp in species.values():
                if sp != "NA":
                    found += 1
            found_species = tk.Label(missing_species_lb_frame, text = str(found), font = ("Open Sans", 18, "bold"), bg = "#2a9d8f", fg = "#f0efeb")
            found_species.grid(row = 0, column = 0, padx = 2)
            missing_species_lb_frame.grid_columnconfigure(1, weight = 1)
            
            string1_lb = tk.Label(missing_species_lb_frame, text = "espèces ont été trouvé pour les", font = ("Open Sans", 18), bg = "#2a9d8f", fg = "#f0efeb")
            string1_lb.grid(row = 0, column = 2)
            missing_species_lb_frame.grid_columnconfigure(3, weight = 1)

            nb_ing_lb = tk.Label(missing_species_lb_frame, text = str(len(ingredients)), font = ("Open Sans", 18, "bold"), bg = "#2a9d8f", fg = "#f0efeb")
            nb_ing_lb.grid(row = 0, column = 4, padx = 2)
            missing_species_lb_frame.grid_columnconfigure(5, weight = 1)

            string2_lb = tk.Label(missing_species_lb_frame, text = "ingrédients.",  font = ("Open Sans", 18), bg = "#2a9d8f", fg = "#f0efeb")
            string2_lb.grid(row = 0, column = 6)

            missing_species_lb_frame.pack(side = "top", expand = 1, anchor = "center", pady = 10)

            info_frame.pack(side = "top", fill = "x", pady = 15)

        # table
            table_frame = tk.Frame(main_frame, bg = "#2a9d8f")

            ing_properties.build_table(ingredients, species, dict_nutrition, dry_matter_dico, name_recipe)
            img = Image.open("assets/figures/" + name_recipe + ".png")
            img_width, img_height = img.size
            self.tables[recipe] = ImageTk.PhotoImage(img)

            table_label = tk.Label(table_frame, image = self.tables[recipe],  bg = "#2a9d8f", height = img_height)
            table_label.pack(expand = 1, fill = "both", anchor = "n")

            table_frame.pack(side = "top", fill = "both", anchor = "n", padx = 30)


        # Results
            bottom_frame = tk.Frame(main_frame, bg = "#2a9d8f")

            results_frame = tk.Frame(bottom_frame, bg = "#2a9d8f")
            results_frame.grid_columnconfigure(0, weight = 1)
        # Phylogenetic diversity
            pd_frame = tk.Frame(results_frame, bg = "#2a9d8f")

            tree = get_lifeMap_subTree.build_tree(species)
            pd = get_dp.phylogenetic_diversity(tree, species)

            pd_info_label = tk.Label(pd_frame, text = "Diversité phylogénétique (MPD, Webb 2002):", \
                font = 'Arial 14 bold', bg = "#2a9d8f", fg = "#f0efeb", justify = "center")
            pd_info_label.pack(side = "top", pady = 5)

            dp_label = ctk.CTkLabel(master = pd_frame, text = pd, text_font = 'Arial 18 bold', fg_color = "#ebf0f8",\
            bg_color = "#2a9d8f", justify = "center", width = 90, height = 90, corner_radius = 5, text_color = "#2c4160")
            dp_label.pack(side = "top")

            pd_frame.grid(row = 0, column = 1, pady = 10, padx = 10)

        # Weighted phylogenetic diversity
            wpd_frame = tk.Frame(results_frame, bg = "#2a9d8f")
            
            dict_sp_drym = {}
            bool_var = True
            for ing in species.keys():
                if species[ing] != "NA":
                    if ing in dry_matter_dico.keys() and dry_matter_dico[ing] != "NA":
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
                bg = "#2a9d8f", fg = "#f0efeb", justify = "center")
            wpd_info_label.pack(side = "top", pady = 5)
           
            wpd_label = ctk.CTkLabel(master = wpd_frame, text = wpd,  text_font = 'Arial 18 bold', fg_color = "#ebf0f8", \
            bg_color = "#2a9d8f", justify = "center", width = 90, height = 90, corner_radius = 5, text_color = "#2c4160")
            wpd_label.pack(side = "top")

            wpd_frame.grid(row = 0, column = 2, pady = 10, padx = 10)

        # Shannon's index
            shannon_frame = tk.Frame(results_frame, bg = "#2a9d8f")
            shannon_info_label = tk.Label(shannon_frame, text = "Indice de Shannon:", font = 'Arial 14 bold', \
                bg = "#2a9d8f", fg = "#f0efeb", justify = "center")
            shannon_info_label.pack(side = "top", pady = 5)
            shannon_label = ctk.CTkLabel(master = shannon_frame, text = shannon, text_font = 'Arial 18 bold', fg_color = "#ebf0f8", \
            bg_color = "#2a9d8f", justify = "center", width = 90, height = 90, corner_radius = 5, text_color = "#2c4160")
            shannon_label.pack(side = "bottom")
            shannon_frame.grid(row = 1, column = 1, pady = 10, padx = 10)

        # Simpson's index
            simpson_frame = tk.Frame(results_frame, bg = "#2a9d8f")
            simpson_info_label = tk.Label(simpson_frame, text = "Indice de Simpson:", font = 'Arial 14 bold', \
                bg = "#2a9d8f", fg = "#f0efeb", justify = "center")
            simpson_info_label.pack(side = "top", pady = 5)
            simpson_label = ctk.CTkLabel(master = simpson_frame, text = simpson, text_font = 'Arial 18 bold', fg_color = "#ebf0f8", \
            bg_color = "#2a9d8f", justify = "center", width = 90, height = 90, corner_radius = 5, text_color = "#2c4160")
            simpson_label.pack(side = "bottom")
            simpson_frame.grid(row = 1, column = 2, pady = 10, padx = 10) 

            results_frame.grid_columnconfigure(3, weight = 1)
            if len(recipes_dict) > 1:
                results_frame.pack(expand = 1, fill = "both", anchor = "n")
            bottom_frame.pack(side = "top", expand = 1, fill = "both", anchor = "center", pady = 20)
            main_frame.pack(expand = 1, fill = "both", anchor = "center")

            temp = recipes_dict[recipe]
            temp.append([pd, wpd, shannon, simpson])
            temp.append(name_recipe)
            recipes_dict[recipe] = temp


    # buttons frame   
        var = tk.StringVar(bottom_frame)
        var.set("Selectionner ...")
        arrow_img = tk.PhotoImage(file = r"assets/download_arrow.png")
        arrow_img = arrow_img.subsample(7, 7)

        if len(recipes_dict) == 1:
            buttons_frame = tk.Frame(bottom_frame, bg = "#2a9d8f")
            buttons_frame.pack(expand = 1, fill = "both", side = "left", anchor= "ne", ipady  = 30)
            results_frame.pack(expand = 1, fill = "both", side = "right", anchor = "nw")
            var.set(name_recipe)

            download = ctk.CTkButton(master = buttons_frame, image = arrow_img,  bg_color = '#2a9d8f', \
            fg_color = "#f0efeb", width = 200, height = 40, corner_radius = 15, hover_color = "#B7B7A4", \
            text_color = "#5aa786", command = lambda: self.download_button(results_window, recipes_dict))
            download.pack(anchor = "center", pady = 10)

        else:
            multi_bottom_frame = tk.Frame(global_frame, bg = "#2a9d8f")
            download_frame = tk.Frame(multi_bottom_frame, bg = "#2a9d8f")
            download_frame.pack(side = "top", expand = 1, fill = "both")
            buttons_frame = tk.Frame(multi_bottom_frame, bg = "#2a9d8f")
            buttons_frame.pack(expand = 1, side = "left", anchor= "e", ipady  = 40, padx = 20)

            choose_frame = tk.Frame(multi_bottom_frame, bg = "#2a9d8f")
            choose_label = tk.Label(choose_frame, text = "Choisir une recette: ", font = ("Open Sans", 20, 'bold'), \
                bg = '#2a9d8f', fg = '#f0efeb')
            choose_label.pack(side = "top", fill = "x")

            options = list(titles.keys())
            choose_optionmenu = tk.OptionMenu(choose_frame, var, *options)
            choose_optionmenu.config(bg = "white", fg = "grey", highlightcolor = "black")
            choose_optionmenu["menu"].config(bg = "white")
            choose_optionmenu.pack(side = "top")

            choose_frame.pack(side = "right", expand = 1, anchor = "w", ipady = 40, padx = 20)
            multi_bottom_frame.pack(side = "bottom", fill = "both", expand = 1, anchor = "center", pady = 20)

            download = ctk.CTkButton(master = download_frame, image = arrow_img,  bg_color = '#2a9d8f', \
            fg_color = "#f0efeb", width = 200, height = 40, corner_radius = 15, hover_color = "#B7B7A4", \
            text_color = "#5aa786", command = lambda: self.download_button(results_window, recipes_dict))
            download.pack(anchor = "center", pady = 30)

        download.image = arrow_img

        lifemap = ctk.CTkButton(master = buttons_frame, text = "LifeMap Tree", text_font =  ("Open Sans", 20, "bold"), \
            bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, height = 50, corner_radius = 12, \
            hover_color = "#B7B7A4", text_color = "#2c4160", command = lambda: self.get_lifemap(var, recipes_dict, titles))
        lifemap.pack(anchor = "center", pady = 10)
        

        # TODO: newick label + 2 buttons: clipboard and download tree

        # try:
        #     os.remove("Tree.txt")
        # except Exception:
        #     pass
        # with open("Tree.txt","w") as Tree:
        #     Tree.write(tree_file)
        #     logger.info("Writing Tree.txt")

        ete = ctk.CTkButton(master = buttons_frame, text = "Ete Sub-tree", text_font =  ("Open Sans", 20, "bold"), \
            bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, height = 50, corner_radius = 12, \
            hover_color = "#B7B7A4", text_color = "#2c4160", command = lambda: self.get_ete(var, recipes_dict, titles, ncbi))
        ete.pack(anchor = "center", pady = 10)


        newick = ctk.CTkButton(master = buttons_frame, text = "Newick Tree", text_font =  ("Open Sans", 20, "bold"), \
            bg_color = '#2a9d8f', fg_color = "#f0efeb", width = 200, height = 50, corner_radius = 12, \
            hover_color = "#B7B7A4", text_color = "#2c4160", command = lambda: self.copy_newick(var, recipes_dict, titles, ncbi))
        newick.pack(anchor = "center", pady = 10)

        global_frame.update_idletasks()       
        global_frame.configure(width = main_canvas.winfo_reqwidth())
        global_frame.pack(fill = "both", expand = 1, anchor = "center")
        main_canvas.configure(yscrollcommand = y_scrollbar.set, highlightthickness = 0)

    # Mousewheel
        global_frame.bind('<Configure>', lambda event: main_canvas.configure(scrollregion = main_canvas.bbox("all")))
        # LinuxOS
        global_frame.bind_all('<Button-4>', lambda event: main_canvas.yview('scroll', -1, 'units'))
        global_frame.bind_all('<Button-5>', lambda event: main_canvas.yview('scroll', 1, 'units'))

        # Windows
        def mouse_wheel(evt):
            if evt.delta == 120:
                main_canvas.yview('scroll', -1, 'units')
            elif evt.delta == -120:
                main_canvas.yview('scroll', 1, 'units')

        global_frame.bind_all('<MouseWheel>', mouse_wheel)

    # create window
        main_canvas.create_window((main_canvas.winfo_reqwidth()/2, 0), window = global_frame, anchor = "nw")


    def download_button(self, window, recipes_dict):
        '''
        Ouvre la fenetre pour nommer le fichier qui aura le tableau au format tsv.
        '''
        try:
            self.download = tk.Toplevel(window)
            self.app = Download(self.download, recipes_dict)
            logger.info("The user has click the download button for the tsv table")
        except Exception:
            logger.exception("Error in opening download window")


    def get_lifemap(self, var, recipes_dict, titles):
        try:
            data = recipes_dict[titles[var.get()]][1]
            if len(data) == 2:
                species = data[0]
            else:
                species = data

            get_lifeMap_subTree.get_subTree(species)
            logger.info("Opening LifeMap page")

        except:
            logger.debug("get_lifemap, recipe don't found or not yet selected")
            pass


    def get_ete(self, var, recipes_dict, titles, ncbi):
        try:
            data = recipes_dict[titles[var.get()]][1]
            if len(data) == 2:
                species = data[0]
            else:
                species = data

            list_ID = get_lifeMap_subTree.get_taxid(species)
            tree = ncbi.get_topology((list_ID), intermediate_nodes = False)
            tree = tree.write(format = 100, features = ["sci_name"]).replace('[&&NHX:sci_name=', '').replace(']', '')
            get_lifeMap_subTree.subtree_from_newick(tree)
            logger.info("The user has click the ete's button")
        except Exception:
            logger.exception("Ete browser doesn't work")


    def copy_newick(self, var, recipes_dict, titles, ncbi):
        try:
            data = recipes_dict[titles[var.get()]][1]
            if len(data) == 2:
                species = data[0]
            else:
                species = data

            list_ID = get_lifeMap_subTree.get_taxid(species)
            tree = ncbi.get_topology((list_ID), intermediate_nodes = False)
            tree = tree.write(format = 100, features = ["sci_name"]).replace('[&&NHX:sci_name=', '').replace(']', '')

            pyperclip.copy(tree)
            logger.info("The user has click the newick's button")
        except:
            logger.debug("Impossible to copy Newick tree")


class Download:
    '''
    Creation de la fenetre qui permet de rentrer le nom du fichier dans lequel on souhaite telecharger le tableau au format csv ou tsv.
    '''
    def __init__(self, download_window, recipes_dict):
        self.download_window = download_window
        
    # window setting 
        download_window.title("Enregistrement")
        w = 700
        h = 250
        x = (download_window.winfo_screenwidth() - w) / 2
        y = (download_window.winfo_screenheight() - h) / 2
        download_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        download_window.minsize(800, 250)
        download_window.config(background = "#2a9d8f")

    # introducing label
        intro_label = tk.Label(download_window, text = "Le fichier sera enregistré dans le répertoire contenant le programme au format tsv.\nChoississez le nom du fichier:", \
                justify = "center", bg = "#2a9d8f", fg = "#f0efeb", font = ("Open Sans", 14))
        intro_label.pack(pady = 20)
   
    # file name entry
        file_name = ctk.CTkEntry(master = download_window, font = ("Open Sans", 12), width = 400, corner_radius = 10)
        file_name.pack(pady = 20)


    # confirm button
        confirm_button = ctk.CTkButton(master = download_window, text = "Enregistrer", text_font = ("Open Sans", 15, "bold"), \
            width = 150, height = 40, command = lambda: self.action(file_name, recipes_dict), bg_color = "#2a9d8f", fg_color = "#f0efeb", \
            hover_color = "#B7B7A4", text_color = "#5aa786", corner_radius = 20)
        confirm_button.pack(pady = 20)

    def action(self, file_name, recipes_dict):
        file_name = file_name.get()
        if not file_name.endswith(".tsv"):
            file_name += ".tsv"
        logger.info("TSV table saved with the filename: " + file_name)
        ing_properties.write_tsv(file_name, recipes_dict)
        self.download_window.withdraw()


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
    with open("log.txt", "r", encoding="utf-8") as log:
        lines = log.readlines()
        log_length = len(lines)
        if log_length > 1000:
            lines = lines[(log_length-1001):-1]

    with open("log.txt", "w", encoding="utf-8") as log:
        for line in lines:
            log.write(line)
except Exception:
    pass
