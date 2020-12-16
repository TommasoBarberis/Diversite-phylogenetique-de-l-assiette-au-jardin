 # -*- coding: utf-8 -*-

from tkinter import *
from tkinter import font
from tkinter import ttk
import requests
from urllib.parse import urlparse
import webbrowser
import get_ing
import ing_to_esp
import ing_properties
import get_lifeMap_subTree
import pyperclip
import get_dp
import get_NCBI_taxonomy
from ete3 import NCBITaxa

class MainWindow:
    '''
    fenetre principale.
    lien vers les sites importantes et champ pour rentrer l'url de la recette a sousmettre.
    '''
    def __init__(self, main_window):
        self.main_window = main_window
        
    # window setting 
        main_window.title("Diversité phylogénétique de l’alimentation")
        main_window.geometry("1080x740")
        main_window.minsize(800,400)
        main_window.config(background="#2a9d8f")

    # title 
        label_title=Label(self.main_window, text="Diversité phylogénétique \nde l’alimentation", font='Helvetica 35 bold', bg='#2a9d8f', fg="#f0efeb")
        label_title.grid(row=1, column=3, pady=10)

        def open_site (url):
            webbrowser.open_new(url)
        def underline (label):
            label.config(font=("Arial", 20, "underline"))
        def desunderline (label):
            label.config(font=("Arial", 20))

    # labels (sites)
        label1=Label(self.main_window, text="Sites optimisés:", font=("Arial", 22, 'bold'), bg='#2a9d8f', fg='#000000')
        label1.grid(row=7, column=3, sticky=W)
        label2=Label(self.main_window, text="\twww.marmitton.org", font=("Arial", 20), bg='#2a9d8f', fg='#f0efeb')
        label2.grid(row=8,column=3, sticky=W)
        label2.bind('<Button-1>', lambda x: open_site("https://www.marmiton.org/"))
        label2.bind('<Enter>', lambda x: underline(label2))
        label2.bind('<Leave>', lambda x: desunderline(label2))
        label3=Label(self.main_window, text="Autres sites implementés:", font=("Arial", 22, 'bold'), bg='#2a9d8f', fg='#000000')
        label3.grid(row=9, column=3, sticky=W)
        label4=Label(self.main_window, text="\twww.750g.com", font=("Arial", 20), bg='#2a9d8f', fg='#f0efeb')
        label4.grid(row=10, column=3, sticky=W)
        label4.bind('<Button-1>', lambda x: open_site("https://www.750g.com/"))
        label4.bind('<Enter>', lambda x: underline(label4))
        label4.bind('<Leave>', lambda x: desunderline(label4))
        label5=Label(self.main_window, text="\twww.cuisineaz.com", font=("Arial", 20), bg='#2a9d8f', fg='#f0efeb')
        label5.grid(row=11, column=3, sticky=W)
        label5.bind('<Button-1>', lambda x: open_site("https://www.cuisineaz.com/"))
        label5.bind('<Enter>', lambda x: underline(label5))
        label5.bind('<Leave>', lambda x: desunderline(label5))

    # gitlab button
        def open_gitlab():
            webbrowser.open_new("http://pedago-service.univ-lyon1.fr:2325/tfroute/div-phylo-alim")
        gitlab_button=Button(self.main_window, text="GitLab", font='arial 20 bold', bg="#f0efeb", fg="#2a9d8f", width=10, command=open_gitlab)
        gitlab_button.grid(row=8, column=1)

    # ucbl button
        def open_ucbl():
            webbrowser.open_new("https://www.univ-lyon1.fr/")
        ucbl_button=Button(self.main_window, text="UCBL", font='arial 20 bold', bg='#f0efeb', fg='#2a9d8f', width=10, command=open_ucbl)
        ucbl_button.grid(row=10,column=1)

    # entry
        label_entry=Label(self.main_window, text="Entrez l'url d'une recette:", font=("Arial", 20, 'bold'), bg='#2a9d8f', fg='#f0efeb')
        label_entry.grid(row=3,column=3, pady=10)
        self.url_entry=Entry(self.main_window, font=("Arial", 20), bg='#2a9d8f', fg='#f0efeb', width=40)
        self.url_entry.grid(row=4,column=3, pady=10)
    # grid
        main_window.grid_rowconfigure(0, weight=1)
        main_window.grid_rowconfigure(2, weight=1)
        main_window.grid_rowconfigure(6, weight=1)
        main_window.grid_rowconfigure(12, weight=1)

        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid_columnconfigure(2, weight=1)
        main_window.grid_columnconfigure(4, weight=1)

    # submit
        submit=Button(self.main_window, text = 'Entrer', font='arial 20 bold', bg='#f0efeb', fg='#2a9d8f', width=12, command=self.test_domain)
        submit.grid(row=5,column=3)
        self.main_window.bind('<Return>', lambda x: self.test_domain()) #ne marche pas

    def test_domain (self):
        '''
        pour tester si l'url est valide, si c'est le cas il ouvre une nouvelle fenetre pour afficher les resultats,
        autrement il affiche une fenetre d'erreur.
        '''
        url=self.url_entry.get()
        domain=""
        try:
            domain=urlparse(url).netloc
        except:
            pass
        if domain=="www.marmiton.org" or domain == "www.750g.com" or domain == "www.cuisineaz.com":   
            self.results_window()
        else:
            self.error_window()
    
    def error_window(self):
        '''
        Ouvre la fenetre d'erreur.
        '''
        self.error=Toplevel(self.main_window)
        self.app=Error(self.error)


    def results_window(self): 
        '''
        Ouvre la fenetre des resultats.
        '''   
        self.results = Toplevel(self.main_window)
        self.app = Results(self.results, url_recipe=self.url_entry.get())

class Error:
    '''
    Creation de la fenetre pour le message d'erreur.
    '''
    def __init__(self, error_window):
        self.error_window=error_window
        
    # window setting 
        error_window.title("Error")
        error_window.geometry("700x200")
        error_window.minsize(700,200)
        error_window.config(background="white")

    # label
        error_message=Label(self.error_window, text="L’URL du site web que vous avez indiquée n’est pas valide. \nVeuillez saisir une URL correcte et réessayez", font='Arial 13 bold', bg='white')
        error_message.grid(row=1, column=1)

    # close button
        def close ():
            error_window.destroy()
        close_button=Button(self.error_window, text="Fermer", command=close)
        close_button.grid(row=3, column=1)

    # grid
        error_window.grid_rowconfigure(0, weight=1)
        error_window.grid_rowconfigure(2, weight=1)
        error_window.grid_rowconfigure(4, weight=1)
        error_window.grid_columnconfigure(0, weight=1)
        error_window.grid_columnconfigure(2, weight=1)

class Results:
    '''
    Creation de la fenetre pour les resulats.
    '''
    def __init__(self, results_window, url_recipe):
        self.results_window=results_window
        self.url_recipe=url_recipe
    
    # window setting 
        results_window.title("Résultats")
        w = results_window.winfo_screenwidth()
        h = results_window.winfo_screenheight()
        results_window.geometry("%dx%d+0+0" % (w, h))
        #results_window.geometry("1600x900")
        results_window.minsize(1080,720)
        results_window.config(background="#C8BFC7")

    #some functions
        def open_site (url):
            webbrowser.open_new(url)
        def underline (label):
            label.config(font=("Arial", 18, "underline"))
        def desunderline (label):
            label.config(font=("Arial", 18))

    # recipe's name 
        name_recipe=get_ing.get_title(self.url_recipe)
        name_recipe=name_recipe[1:]
        label1=Label(self.results_window, text="Nom de la recette: ", font='Arial 18 bold', bg='#C8BFC7', fg="#8A7E72")
        label1.grid(row=1, column=1, sticky=W, columnspan=6)
        recipe=Label(self.results_window, text=name_recipe, font='Arial 18', bg='#C8BFC7', fg="#000000", justify=LEFT)
        recipe.grid(row=1, column=3, sticky=W, columnspan=6)
    
        ingredients=get_ing.process(self.url_recipe)
        species=ing_to_esp.recherche_globale(ingredients)

    # missing species
        string1="{} espèces ont été trouvé pour les {} ingrédients.".format(len(species),len(ingredients))
        missing_species1=Label(self.results_window, text=string1, font='Arial 18 bold', bg='#C8BFC7', fg="#8A7E72")
        missing_species1.grid(row=3, column=1, sticky=W, columnspan=6)
        missing_sp_list=missing_species(ingredients,species)
        if not missing_sp_list[1]:
            missing_species2=Label(self.results_window, text="Les ingrédients pour lesquels l’espèce manque:", font='Arial 18 bold', bg='#C8BFC7', fg="#8A7E72")
            missing_species2.grid(row=4, column=1, sticky=W, columnspan=6)
            save_row=5
            for add, sp in enumerate(missing_sp_list[0]):
                save_row+=add
                missing=Label(self.results_window, text="\t"+sp, font='Arial 18', bg='#C8BFC7', fg="#000000")
                missing.grid(row=save_row, column=1, sticky=W, columnspan=6)
        else:
            not_missing=Label(self.results_window, text="Aucune espèce manque", font='Arial 18', bg='#C8BFC7', fg="#000000")

    # missing ingredients in nutritional db
        missing_ing_list=missing_nutrition(ingredients)
        string2="{}/{} ingrédients ont été trouvé dans la table Ciqual (base de données).".format(str(len(ingredients)-len(missing_ing_list[0])),len(ingredients))
        missing_ing1=Label(self.results_window, text=string2, font='Arial 18 bold', bg='#C8BFC7', fg="#8A7E72")
        save_row+=1
        missing_ing1.grid(row=save_row, column=1, sticky=W, columnspan=6)
        if not missing_ing_list[1]: 
            missing_ing2=Label(self.results_window, text="Ingrédients pour lesquels aucune information a été trouvé:", font='Arial 18 bold', bg='#C8BFC7', fg="#8A7E72")
            save_row+=1
            missing_ing2.grid(row=save_row, column=1, sticky=W, columnspan=6)
            save_row+=1
            for add1, ing in enumerate(missing_ing_list[0]):
                save_row+=add1
                missing1=Label(self.results_window, text="\t"+ing, font='Arial 18', bg='#C8BFC7', fg="#000000")
                missing1.grid(row=save_row, column=1, sticky=W, columnspan=6)

    # table
        dict_row=table_row(ingredients, species)
        list_column=["Ingrédient","Espèce","Quantité","Qté de matière\n sèche (g)","Glucides (%)","Lipides (%)","Sucres (%)","Protéines (%)"]
        save_row+=1

        for i in range(len(list_column)):
            if i==2:
                table_header=Label(self.results_window, text=list_column[i], font="Arial 14", bg='#C8BFC7', fg="#090302", justify=CENTER, relief=GROOVE, width=11, height=3)
            elif i==3:
                table_header=Label(self.results_window, text=list_column[i], font="Arial 14", bg='#C8BFC7', fg="#090302", justify=CENTER, relief=GROOVE, width=16, height=3)
            elif i==4:
                table_header=Label(self.results_window, text=list_column[i], font="Arial 14", bg='#C8BFC7', fg="#090302", justify=CENTER, relief=GROOVE, width=14, height=3)
            elif i==5:
                table_header=Label(self.results_window, text=list_column[i], font="Arial 14", bg='#C8BFC7', fg="#090302", justify=CENTER, relief=GROOVE, width=14, height=3)
            elif i==6:
                table_header=Label(self.results_window, text=list_column[i], font="Arial 14", bg='#C8BFC7', fg="#090302", justify=CENTER, relief=GROOVE, width=13, height=3)
            else:
                table_header=Label(self.results_window, text=list_column[i], font="Arial 14", bg='#C8BFC7', fg="#090302", justify=CENTER, relief=GROOVE, width=18, height=3) 
            table_header.grid(row=save_row, column=1+i, sticky=W)
        for j in dict_row.keys():
            line=dict_row[j]
            save_row+=1
            for ind, k in enumerate(line):
                if ind==2:
                    table_cell=Label(self.results_window, text=k, font="Arial 14", bg='#C8BFC7', fg="#000000", justify=CENTER, relief=GROOVE, width=11, wraplength=300, height=2)
                elif ind==3:
                    table_cell=Label(self.results_window, text=k, font="Arial 14", bg='#C8BFC7', fg="#000000", justify=CENTER, relief=GROOVE, width=16, wraplength=300, height=2)
                elif ind==4:
                    table_cell=Label(self.results_window, text=k, font="Arial 14", bg='#C8BFC7', fg="#000000", justify=CENTER, relief=GROOVE, width=14, wraplength=300, height=2)
                elif ind==5:
                    table_cell=Label(self.results_window, text=k, font="Arial 14", bg='#C8BFC7', fg="#000000", justify=CENTER, relief=GROOVE, width=14, wraplength=300, height=2)
                elif ind==6:
                    table_cell=Label(self.results_window, text=k, font="Arial 14", bg='#C8BFC7', fg="#000000", justify=CENTER, relief=GROOVE, width=13, wraplength=300, height=2)
                else:
                    table_cell=Label(self.results_window, text=k, font="Arial 14", bg='#C8BFC7', fg="#000000", justify=CENTER, relief=GROOVE, width=18, wraplength=300, height=2)
                table_cell.grid(row=save_row, column=1+ind, sticky=W)

        #results_window.rowconfigure(save_row+1, weight=1)
        save_row+=2

    # buttons
        def enter_download():
            label_photo_info.config(text='Télécharger le tableau au format tsv')
        def leave_download():
            label_photo_info.config(text="")
        photo=PhotoImage(file = r"download_arrow.png")
        sub_photo=photo.subsample(7,7)
        download=Button(self.results_window, image=sub_photo,  bg='#8A7E72', width=40, height=40, command=self.download_button)
        download.image=sub_photo
        download.grid(row=save_row-1, column=0, pady=10, columnspan=3)
        download.bind('<Enter>', lambda x: enter_download())
        download.bind('<Leave>', lambda x: leave_download())
        label_photo_info=Label(self.results_window, text="", bg='#C8BFC7', fg="#8A7E72")
        label_photo_info.grid(row=save_row, column=1, columnspan=2, sticky=N)

        def get_lifemap (especes):
            get_lifeMap_subTree.get_subTree(especes)
        lifemap=Button(self.results_window, text="LifeMap Tree", font="arial 20 bold", bg='#8A7E72', fg="#5A2328", width=12)
        lifemap.grid(row=save_row, column=3, pady=10, sticky=W, columnspan=2)
        lifemap.bind('<Button-1>', lambda x: get_lifemap(species))
        
        save_row+=1

        list_ID = get_NCBI_taxonomy.get_taxid(species)
        ncbi=NCBITaxa()
        tree=ncbi.get_topology((list_ID), intermediate_nodes=True)
        tree=tree.write(format=100, features=["sci_name"]).replace('[&&NHX:sci_name=','').replace(']','')
        try:
            os.remove("Tree.txt")
        except :
            pass
        with open("Tree.txt","w") as Tree:
            Tree.write(tree)

        def get_ete ():
            get_lifeMap_subTree.subtree_from_newick()
        ete=Button(self.results_window, text="Ete Sub-tree", font="arial 20 bold", bg='#8A7E72', fg="#5A2328", width=12)
        ete.grid(row=save_row, column=3, pady=10, sticky=W, columnspan=2)
        ete.bind('<Button-1>', lambda x: get_ete())

        save_row+=1

        def get_newick ():
            with open ("Tree.txt","r") as tree:
                newick_tree=str(tree.readlines())
                pyperclip.copy(newick_tree)
        newick=Button(self.results_window, text="Newick Tree", font="arial 20 bold", bg='#8A7E72', fg="#5A2328", width=12)
        newick.grid(row=save_row, column=3, pady=10, sticky=W, columnspan=2)
        newick.bind('<Button-1>', lambda x: get_newick())

        def enter_button():
            label_info.config(text='Le bouton "Newick Tree" \npermet de recopier le sous-arbre \nde newick dans le clipboard')
        def leave_button():
            label_info.config(text="")
        label_info=Label(self.results_window, text="", bg='#C8BFC7', fg="#8A7E72", width=40)
        label_info.grid(row=save_row, column=5, columnspan=3, sticky=W)
        newick_info=Button(self.results_window, text="?", font="arial 20 bold", bg='#8A7E72', fg="#5A2328", width=2)
        newick_info.grid(row=save_row, column=4, pady=10, sticky=E)
        newick_info.bind('<Enter>', lambda x: enter_button())
        newick_info.bind('<Leave>', lambda x: leave_button())

    # DP
        dp=get_dp.calculation("Tree.txt")
        label6=Label(self.results_window, text="Diversité phylogénétique (en nb de branches):", font='Arial 14 bold', bg='#C8BFC7', fg="#8A7E72")
        label6.grid(row=save_row-2, column=5, columnspan=4, sticky=W)
        dp_label=Label(self.results_window, text=dp, font='Arial 18 bold', bg='#C8BFC7', fg="#090302", justify=CENTER, relief=RAISED, width=7, height=3)
        dp_label.grid(row=save_row-1, column=5, columnspan=4)

    # grid
        results_window.rowconfigure(0, weight=1)
        results_window.rowconfigure(save_row+1, weight=1)

        results_window.grid_columnconfigure(0, weight=1)
        results_window.grid_columnconfigure(8, weight=1)

    def download_button (self):
        self.file_name_window()

    def file_name_window(self):
        '''
        Ouvre la fenetre pour nommer le fichier qui aura le tableau au format tsv.
        '''
        self.download=Toplevel(self.results_window)
        self.app=Download(self.download, url_recipe=self.url_recipe)

class Download:
    '''
    Creation de la fenetre qui permet de rentrer le nom du fichier dans lequel on souhaite telecharger le tableau au format csv ou tsv.
    '''
    def __init__(self, download_window, url_recipe):
        self.download_window=download_window
        self.url_recipe=url_recipe
        
    # window setting 
        download_window.title("Enregistrement")
        download_window.geometry("700x200")
        download_window.minsize(800,200)
        download_window.config(background="#C8BFC7")
        download_window.grid_rowconfigure(0, weight=1)

    # introducing label
        intro_label=Label(self.download_window, text="Le fichier sera enregistré dans le répertoire contenant le programme au format tsv.\nChoississez le nom du fichier:", font="arial 11", bg="#C8BFC7", justify=CENTER)
        intro_label.grid(row=1, column=1)
    # file name entry
        file_name=Entry(self.download_window, font="arial 11", width=40)
        file_name.grid(row=2, column=1)

        download_window.grid_rowconfigure(3, weight=1)

    # confirm button
        ingredients=get_ing.process(self.url_recipe)
        species=ing_to_esp.recherche_globale(ingredients)
        dico_nut=ing_properties.getDictNut(ingredients)
        dry_dico=ing_properties.dryMatterDicUpdate(ingredients, dico_nut)

        def action (file_name):
            file_name=file_name.get()
            if not file_name.endswith(".tsv"):
                file_name+=".tsv"
            ing_properties.writeTsv(file_name,ingredients,species,dry_dico,dico_nut)
            self.download_window.destroy()
        confirm_button=Button(self.download_window, text="Enregistrer", font="arial 11", width=10)
        confirm_button.grid(row=4, column=1)
        confirm_button.bind("<Button-1>", lambda x: action(file_name))

        download_window.grid_rowconfigure(5, weight=1)
        download_window.grid_columnconfigure(0, weight=1)
        download_window.grid_columnconfigure(2, weight=1)

def missing_species(ingredients, especes):
    species_not_found = []
    if len(ingredients) != len(especes) :
        complete_spec = False
        for key in ingredients:
            if key not in especes and key[:-1] not in especes.keys():
                species_not_found.append(key)
    else : complete_spec = True
    return (species_not_found, complete_spec)

def missing_nutrition (ingredients):
    dictionnaire_nutrition = ing_properties.getDictNut(ingredients)
    nbnut =len(dictionnaire_nutrition)
    nut_not_found = []
    if len(ingredients) != nbnut :
        complete_nut = False
        for key in ingredients:
            if key.capitalize() not in dictionnaire_nutrition:
                nut_not_found.append(key.capitalize())
    else : complete_nut = True
    return (nut_not_found, complete_nut)

def table_row (ingredients, especes):
    dictionnaire_nutrition = ing_properties.getDictNut(ingredients)
    dict_row={}
    for key in ingredients.keys():
        ing=str(key)
        if ing.endswith("s"):
            ing=ing[:-1]
        list_row=[ing]
        if ing in especes.keys():
            list_row.append(especes[ing])
        else:
            list_row.append("-")
        list_row.append(ingredients[key])
        if ing.capitalize() in dictionnaire_nutrition.keys():
            for i, val in enumerate(dictionnaire_nutrition[ing.capitalize()]):
                if i==0:
                    pass
                else:
                    list_row.append(val)
        else:
            for k in range(5):
                list_row.append("-")
        dict_row[ing]=list_row
    return dict_row

def main(): 
    root = Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()