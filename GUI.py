 # -*- coding: utf-8 -*-

from tkinter import *
from tkinter import font
import requests
from urllib.parse import urlparse
import webbrowser
#from PIL import Image, ImageTk

class MainWindow:
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

        # label (sites)
        label1=Label(self.main_window, text="Sites optimisés:", font=("Arial", 22, 'bold'), bg='#2a9d8f', fg='#656565')
        label1.grid(row=7, column=3, sticky=W)
        label2=Label(self.main_window, text="\twww.marmitton.org", font=("Arial", 20), bg='#2a9d8f', fg='#f0efeb')
        label2.grid(row=8,column=3, sticky=W)
        label2.bind('<Button-1>', lambda x: open_site("https://www.marmiton.org/"))
        label2.bind('<Enter>', lambda x: underline(label2))
        label2.bind('<Leave>', lambda x: desunderline(label2))
        label3=Label(self.main_window, text="Autres sites implementés:", font=("Arial", 22, 'bold'), bg='#2a9d8f', fg='#656565')
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
        gitlab_button=Button(self.main_window, text="GitLab", font='button_font 20 bold', bg="#f0efeb", fg="#2a9d8f", width=10, command=open_gitlab)
        gitlab_button.grid(row=8, column=1)

        # ucbl button
        def open_ucbl():
            webbrowser.open_new("https://www.univ-lyon1.fr/")
        ucbl_button=Button(self.main_window, text="UCBL", font='button_font 20 bold', bg='#f0efeb', fg='#2a9d8f', width=10, command=open_ucbl)
        ucbl_button.grid(row=10,column=1)

        # entry
        label_entry=Label(self.main_window, text="Entrez l'url d'une recette:", font=("Arial", 20, 'bold'), bg='#2a9d8f', fg='#f0efeb')
        label_entry.grid(row=3,column=3, pady=10)
        self.url_entry=Entry(self.main_window, font=("Arial", 20), bg='#2a9d8f', fg='#f0efeb', width=40)
        self.url_entry.grid(row=4,column=3, pady=10)
    
        main_window.grid_rowconfigure(0, weight=1)
        main_window.grid_rowconfigure(2, weight=1)
        main_window.grid_rowconfigure(6, weight=1)
        main_window.grid_rowconfigure(12, weight=1)

        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid_columnconfigure(2, weight=1)
        main_window.grid_columnconfigure(4, weight=1)

        # submit
        submit=Button(self.main_window, text = 'Entrer', font='Helvetica 20 bold', bg='#f0efeb', fg='#2a9d8f', width=12, command=self.test_domain)
        submit.grid(row=5,column=3)

    def test_domain (self):
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
        self.error=Toplevel(self.main_window)
        self.app=Error(self.error)


    def results_window(self):    
        self.results = Toplevel(self.main_window)
        self.app = Results(self.results)

class Error:
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

        error_window.grid_rowconfigure(0, weight=1)
        error_window.grid_rowconfigure(2, weight=1)
        error_window.grid_rowconfigure(4, weight=1)
        error_window.grid_columnconfigure(0, weight=1)
        error_window.grid_columnconfigure(2, weight=1)


class Results:
    def __init__(self, newWindow):
        self.newWindow=newWindow
    

def main(): 
    root = Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()