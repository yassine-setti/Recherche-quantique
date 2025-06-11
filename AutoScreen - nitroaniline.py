# Importation des modules nécessaires
import subprocess  # Permet d'exécuter des processus externes et de communiquer avec eux.
import pyautogui   # Utilisé pour simuler des interactions utilisateur avec l'écran, comme les clics et les frappes.
import time        # Fournit des fonctions pour gérer le temps.
from PIL import ImageGrab   # Pour effectuer des captures d'écran.
import os          # Pour interagir avec le système d'exploitation.
import tkinter as tk  # Utilisé pour la création d'interfaces graphiques.
import cv2         # Utilisé pour le traitement d'images.
from tkinter import ttk # Pour utiliser la barre de progression.


### La fonction qui suit exécute le programme MultiWFN :

def MultiWFN_exe(file_path, commands):
    # Définit le chemin absolu de l'exécutable Multiwfn
    application_path = r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\Multiwfn_3.8_dev_bin_Win64/Multiwfn.exe"

    # Lance Multiwfn avec un fichier spécifique et initialise la communication avec subprocess
    process = subprocess.Popen(
        [application_path, file_path], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )

    # Exécution des commandes dans Multiwfn
    for command in commands:
        process.stdin.write(command + '\n')  # Envoie chaque commande au processus
    process.stdin.close()  # Indique la fin des commandes

    # Attente de la fin de l'exécution et récupération des sorties
    stdout, stderr = process.communicate()

    # Affiche la sortie standard de Multiwfn
    print("Sortie de Multiwfn:")
    print(stdout)
    
    # Affiche les éventuelles erreurs
    if stderr:
        print("Erreurs:")
        print(stderr)


## Génération dynamique de la liste des fichiers .wfn à traiter
files = []  # Liste vide pour stocker les chemins des fichiers

## Définition des paramètres de base pour localiser les fichiers
base_path = r'D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\4nitroaniline\4nitroaniline_NO2'
file_prefix = '4nitroaniline'
file_extension = '.wfn'

## Boucle pour générer les chemins des fichiers (de 1 à 40)
for i in range(1, 41):
    file_name = f"{file_prefix}{i}{file_extension}"  # Nom du fichier
    full_path = f"{base_path}\\{file_name}"         # Chemin complet
    files.append(full_path)                         # Ajoute le chemin à la liste

# Vérification en affichant tous les chemins
for file in files:
    print(file)



### Définition des commandes pour Multiwfn selon différentes analyses ###

# Commandes pour soustraire la densité électronique
commands_densite=['4','0','1',r'-,D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\4nitroaniline\4nitroaniline_NO2\4nitroaniline2.wfn','1','2','200,200','1','0.2','1','-0.005,0.005','0','q']

# Commandes pour afficher les bassins atomiques
commands_surface_interbassins = ['2', '2', '3', '8', '10', '0', 'q', '0','q']

# Commandes pour afficher la densité électronique sur un chemin interbassin
commands_surface_densitechemin =['2','2','3','8','10','0','q','0','-5','7', '(11,12)','1']

# Commandes pour effectuer une analyse électrophile
commands_electrophyle= ['22','3','3','4']

# Liste des chemins spécifiques pour les analyses interbassins
chemindensite=['(11,12)' , '(29,30)' , '(35,36)' , '(27,28)' , '(13,14)' , '(9,10)']

valeur=0 # Variable utilisée pour stocker certaines valeurs d'entrée utilisateur

# Liste des chemins spécifiques pour les analyses interbassins
commands_raman=['11','2','0','q']

######Fonction des boutons Tkinter##########
from video import create_video_from_images 
def commands_densite_func():
        num_files = len(files)
        # Initialiser la barre de progression
        progress_bar["maximum"] = num_files
        progress_bar["value"] = 0
        for index, file in enumerate(files): #pour chaque fichier WFN
            print(f"Traitement de {files}...")
            #commands_densite =  commands_densite_creation(index,files)
            MultiWFN_exe(file, commands_densite) # Exécute MultiWFN avec les commandes associées
            # Mettre à jour la barre de progression
            progress_bar["value"] = index + 1
            progress_bar.update()
            print(f"{files} terminé.\n")
        # Création de la vidéo issue de l'exécution
        create_video_from_images(r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique",r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique\videoaniline\output_videodensite.mp4",10)

## Fonction pour afficher les surfaces des bassins atomiques
def commands_surface_interbassins_func():
            num_files = len(files)
            # Initialiser la barre de progression
            progress_bar["maximum"] = num_files
            progress_bar["value"] = 0
            for index, file in enumerate(files): #pour chaque fichier WFN
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, commands_surface_interbassins) # Exécute MultiWFN avec les commandes associées
                # Mettre à jour la barre de progression
                progress_bar["value"] = index + 1
                progress_bar.update()
                print(f"{file} terminé.\n")
            # Création de la vidéo issue de l'exécution
            create_video_from_images(r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique",f"D:\\Users\\Hugo\\SynologyDrive\\CentraleSupelec\\2A\\Cours\\ProjetENTRAVE\\densiteelectronique\\videoaniline\\output_videosurfaceinterbassins.mp4",10)

## Fonction pour afficher la densité électronique sur un chemin interbassin
def commands_surface_densitechemin_func():
    for i in chemindensite:
        num_files = len(files)
        # Initialiser la barre de progression
        progress_bar["maximum"] = num_files
        progress_bar["value"] = 0
        for index, file in enumerate(files): #pour chaque fichier WFN
            print(f"Traitement de {file}...")
            MultiWFN_exe(file, commands_surface_densitechemin) # Exécute MultiWFN avec les commandes associées
            # Mettre à jour la barre de progression
            progress_bar["value"] = index + 1
            progress_bar.update()
            print(f"{file} terminé.\n")
        # Création de la vidéo issue de l'exécution
        create_video_from_images(r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique",r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique\videoaniline\output_videosurfacedensitechemin{i}.mp4",10)

## Fonction pour effectuer une analyse électrophile
def commands_electrophyle_func():
        num_files = len(files)
        # Initialiser la barre de progression
        progress_bar["maximum"] = num_files
        progress_bar["value"] = 0
        for index, file in enumerate(files): #pour chaque fichier WFN
            print(f"Traitement de {file}...")
            MultiWFN_exe(file, commands_electrophyle) # Exécute MultiWFN avec les commandes associées
             # Mettre à jour la barre de progression
            progress_bar["value"] = index + 1
            progress_bar.update()
            print(f"{file} terminé.\n")
        # Création de la vidéo issue de l'exécution
        create_video_from_images(r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique",r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique\videoaniline\output_videoelectrophyle.mp4",10)

## Fonction pour afficher une orbitale spécifique (avec valeur entrée par l'utilisateur)
def commands_orbitale_func():
    # Récupérer la valeur de l'entrée
    numorbitale = orbitaleentry.get()
    isoval=orbisovalueentry.get()
    num_files = len(files)
    # Initialiser la barre de progression
    progress_bar["maximum"] = num_files
    progress_bar["value"] = 0
    for index, file in enumerate(files): #pour chaque fichier WFN
        print(f"Traitement de {file}...")
        # Appeler la fonction MultiWFN_exe avec les paramètres
        MultiWFN_exe(file, ['5', '4', str(numorbitale), '3', '4', str(isoval), '1', 'q']) # Exécute MultiWFN avec les commandes associées
        # Mettre à jour la barre de progression
        progress_bar["value"] = index + 1
        progress_bar.update()
        print(f"{file} terminé.\n")
    # Création de la vidéo issue de l'exécution
    create_video_from_images(r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique",f"D:\\Users\\Hugo\\SynologyDrive\\CentraleSupelec\\2A\\Cours\\ProjetENTRAVE\\densiteelectronique\\videoaniline\\output_videoorbitale{numorbitale}.mp4",10)
    print("Traitement complet. Vidéo créée.")


## Fonction pour effectuer une analyse de Raman
def commands_raman_func():
        num_files = len(files)
        # Initialiser la barre de progression
        progress_bar["maximum"] = num_files
        progress_bar["value"] = 0
        for index, file in enumerate(files): #pour chaque fichier WFN
            print(f"Traitement de {file}...")
            MultiWFN_exe(file, commands_raman) # Exécute MultiWFN avec les commandes associées
             # Mettre à jour la barre de progression
            progress_bar["value"] = index + 1
            progress_bar.update()
            print(f"{file} terminé.\n")
        # Création de la vidéo issue de l'exécution
        create_video_from_images(r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique",r"D:\Users\Hugo\SynologyDrive\CentraleSupelec\2A\Cours\ProjetENTRAVE\densiteelectronique\videoaniline\output_videoelectrophyle.mp4",10)

### Création de l'interface Tkinter ###
def close():
    root.destroy() # Ferme l'interface graphique

## Création de la fenêtre principale
root = tk.Tk()
root.title("Menu des commandes") # Titre de la fenêtre
root.geometry("1700x900") # Dimensions de la fenêtre
root.configure(bg="chocolate") # Couleur de fond

## Configuration des widgets Tkinter
tk.Label(root).grid(row=0, column=0, pady=10) #grille pour placer les bouttons

## Fonction appelée lors de l'exécution d'une commande personnalisée
def callback():
    valeur = entry.get() # Récupère la commande entrée par l'utilisateur
    for file in files:
            print(f"Traitement de {file}...")
            MultiWFN_exe(file, valeur) # Exécute MultiWFN avec la commande entrée
            print(f"{file} terminé.\n")
    else:
        print("Commande inconnue")

### Chargement des images pour les boutons ###
imagedens = tk.PhotoImage(file="imagedens.png").subsample(5, 5)
imagebassin = tk.PhotoImage(file="imagebassin.png").subsample(3, 3)
imagechemin = tk.PhotoImage(file="imagechemin.png").subsample(3, 3)
imageorbitale = tk.PhotoImage(file="imageorbitale.png").subsample(5, 5)

########## Implémentation des boutons##########
button_width = 40
frame_width = 800  # Largeur fixe pour tous les frames
frame_height = 400  # Hauteur fixe pour tous les frames

#commande personnalisée
# Création du cadre
frame_personnal = tk.Frame(root, bg="orange", width=frame_width, height=frame_height, padx=10, pady=10, bd=5, relief="ridge")  
frame_personnal.grid(row=0, column=0, padx=20, pady=20, columnspan=3)
#Bouton pour entrée une commande spécifique ( sous la forme d'une liste ['1','2',...])
tk.Label(frame_personnal, text="Entrez la commande souhaitée",bg="orange",fg="white",width=button_width).grid(row=0, column=1, padx=5)
entry = tk.Entry(frame_personnal,width=button_width)
entry.grid(row=1, column=1, padx=5)
tk.Button(frame_personnal, text="Exécuter", command=callback,bg="coral",fg="white",width=button_width).grid(row=2, column=1, padx=5)
#bouton pour la soustraction de densité électronique
# Création du cadre
frame_densite = tk.Frame(root, bg="orange", width=frame_width, height=frame_height, padx=10, pady=10, bd=5, relief="ridge")  
frame_densite.grid(row=1, column=0, padx=20, pady=20, columnspan=3)
# Ajout des widgets dans le cadre
imagedens = tk.PhotoImage(file="imagedens.png").subsample(5, 5)  # Exemple d'image
tk.Button(frame_densite, text="Soustraction de la densité électronique", command= commands_densite, image=imagedens, compound="left", bg="coral", fg="white", padx=5, pady=5).grid(row=1, column=0, padx=5, rowspan=4, columnspan=2)
tk.Label(frame_densite, text="Entrez l'isovalue souhaitée", bg="orange", fg="white", width=button_width).grid(row=1, column=2, padx=5)
densiteisovalueentry = tk.Entry(frame_densite, width=button_width)
densiteisovalueentry.grid(row=2, column=2, padx=5)

#bouton pour les surfaces des bassins atomiques
# Création du cadre
frame_bassinsatomiques= tk.Frame(root, bg="orange", width=frame_width, height=frame_height, padx=10, pady=10, bd=5, relief="ridge")  
frame_bassinsatomiques.grid(row=2, column=3, padx=20, pady=20, columnspan=3)
# Ajout des widgets dans le cadre
tk.Button(frame_bassinsatomiques, text="Surface des bassins atomiques", command=commands_surface_interbassins_func,image=imagebassin, compound="left",bg="coral",fg="white",padx=5,pady=5).grid(row=3, column=3, padx=5,rowspan=4, columnspan=2)

#bouton pour les surfaces des chemins
# Création du cadre
frame_chemin= tk.Frame(root, bg="orange", width=frame_width, height=frame_height, padx=10, pady=10, bd=5, relief="ridge")  
frame_chemin.grid(row=2, column=0, padx=20, pady=20, columnspan=3)
# Ajout des widgets dans le cadre
tk.Button(frame_chemin, text="Densité électronioque sur un chemin interbassin", command=commands_surface_densitechemin_func,image=imagechemin, compound="left",bg="coral",fg="white",padx=5,pady=5).grid(row=7, column=0, padx=5,rowspan=4, columnspan=2)


#bouton pour l'intensité de Raman
# Création du cadre
frame_Raman= tk.Frame(root, bg="orange", width=frame_width, height=frame_height, padx=10, pady=10, bd=5, relief="ridge")  
frame_Raman.grid(row=3, column=0, padx=20, pady=20, columnspan=3)
tk.Button(frame_Raman, text="Intensité de Raman", command=commands_raman_func,bg="coral",fg="white",width=button_width).grid(row=7, column=3, padx=5)

#affichage des orbitales##
# Création du cadre
frame_orbitales= tk.Frame(root, bg="orange", width=frame_width, height=frame_height, padx=10, pady=10, bd=5, relief="ridge")  
frame_orbitales.grid(row=1, column=3, padx=20, pady=20, columnspan=3)
tk.Button(frame_orbitales, text="Affichage de l'orbitale souhaitée", command=commands_orbitale_func,bg="coral",fg="white",image=imageorbitale, compound="left",padx=5,pady=5).grid(row=11, column=0, padx=5,rowspan=4, columnspan=2)
#choix de l'orbitale à afficher
tk.Label(frame_orbitales, text="Entrez l'orbitale souhaitée",bg="orange",fg="white",width=button_width).grid(row=11, column=2, padx=5)
orbitaleentry=tk.Entry(frame_orbitales,text="Orbitale souhaitée",width=button_width)
orbitaleentry.grid(row=12, column=2)
#choix de l'isovalue de l'orbitale
tk.Label(frame_orbitales, text="Entrez l'isovalue souhaitée",bg="orange",fg="white",width=button_width).grid(row=13, column=2,padx=5)
orbisovalueentry=tk.Entry(frame_orbitales,text="isovalue de l'orbitale souhaitée",width=button_width)
orbisovalueentry.grid(row=14, column=2,padx=5)


# Barre de progression
# Création du cadre
frame_progress= tk.Frame(root, bg="orange", width=frame_width, height=frame_height, padx=10, pady=10, bd=5, relief="ridge")  
frame_progress.grid(row=0, column=3, padx=20, pady=20, columnspan=3)
#barre de progression
tk.Label(frame_progress, text="Progress",bg="orange",fg="white",width=button_width).grid(row=3, column=3,padx=5)
progress_bar = ttk.Progressbar(frame_progress, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=4, column=3, padx=5)
###bouton de fermeture#####
tk.Button(frame_progress, text="Quitter", command=close,bg="red",fg="white",width=button_width).grid(row=5, column=3, padx=5)


root.mainloop()



