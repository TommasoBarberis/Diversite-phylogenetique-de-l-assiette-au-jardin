from tkinter import *
from tkinter import font
import webbrowser
#from PIL import Image, ImageTk

# window generation
window=Tk()

# window settings
window.title("Diversité phylogénétique de l’alimentation")
window.geometry("1080x740")
window.minsize(800,400)
window.config(background="#2a9d8f")

# title
label_title=Label(window, text="Diversité phylogénétique \nde l’alimentation", font='Helvetica 35 bold', bg='#2a9d8f', fg="#f0efeb")
label_title.grid(row=1, column=3, pady=10, columnspan=5)

# buttons
button_font=font.Font(font='times')

# gitlab button
def open_gitlab():
    webbrowser.open_new("http://pedago-service.univ-lyon1.fr:2325/tfroute/div-phylo-alim")
gitlab_button=Button(window, text="GitLab", font='button_font 20 bold', bg="#f0efeb", fg="#2a9d8f", width=10, command=open_gitlab)
gitlab_button.grid(row=7, column=1)


# ucbl button
def open_ucbl():
    webbrowser.open_new("https://www.univ-lyon1.fr/")
ucbl_button=Button(window, text="UCBL", font='button_font 20 bold', bg='#f0efeb', fg='#2a9d8f', width=10, command=open_ucbl)
ucbl_button.grid(row=9,column=1)

# entry
#label_title=Label(entry_frame, text="Entrez l'url d'une recette:", font=("Arial", 20, 'bold'), bg='#2a9d8f', fg='#f0efeb')
#label_title.pack(pady=5)
url_entry=Entry(window, text="Entrez l'url d'une recette", font=("Arial", 20), bg='#2a9d8f', fg='#f0efeb', width=50)
url_entry.grid(row=3,column=3, pady=10, columnspan=5)

# submit buttons
import get_lifeMap_subTree
import get_ing
import ing_to_esp
import get_dp
import ing_properties
import os

def lifemap():
    url=url_entry.get()
    ingredients = get_ing.process(url)
    especes = ing_to_esp.recherche_globale(ingredients)
    get_lifeMap_subTree.get_subTree(especes)
    
lifemap_button=Button(window, text="LifeMap Tree", font='Helvetica 20 bold', bg='#f0efeb', fg='#2a9d8f', width=12, command=lifemap)
lifemap_button.grid(row=5, column=3)

def ete():
    url=url_entry.get()
    ingredients = get_ing.process(url)
    especes = ing_to_esp.recherche_globale(ingredients)
    get_lifeMap_subTree.get_newick(especes)
    get_lifeMap_subTree.subtree_from_newick()

ete_button=Button(window, text="ETE Sub-tree", font='Helvetica 20 bold', bg='#f0efeb', fg='#2a9d8f', width=12, command=ete)
ete_button.grid(row=5, column=5)

def new_window():
    window2=Toplevel(window)
    window2.title("Results")
    window2.geometry("1080x740")
    window.minsize(800,400)
    window2.config(background="#a7c957")


result_button=Button(window, text="Results", font='Helvetica 20 bold', bg='#f0efeb', fg='#2a9d8f', width=12, command=new_window)
result_button.grid(row=5,column=7)

window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(6, weight=1)
window.grid_rowconfigure(8, weight=1)
window.grid_rowconfigure(10, weight=1)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(4, weight=1)
window.grid_columnconfigure(6, weight=1)
window.grid_columnconfigure(8, weight=1)
window.mainloop()