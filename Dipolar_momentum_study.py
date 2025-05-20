from tkinter import *
import tkinter.filedialog
import numpy as np
import subprocess
import pyautogui
import time
from PIL import ImageGrab
import os
import shutil
import cv2
import matplotlib.pyplot as plt

############################################################################################################
############################################################################################################
##                                                                                                        ##
##                                                                                                        ##
##                                        Dipolar Momentum Study                                          ##
##                                                                                                        ##
##                                                                                                        ##
############################################################################################################
############################################################################################################

## Définition des fonctions

def MultiWFN_exe(file_path, commands):
    ''' Exécute MultiWFN avec les commandes spécifiées '''

    # Chemin de l'application MultiWFN
    application_path = r"/Users/antoinecs/multiwfn-mac-build/Multiwfn"

    try:
        # Ouvrir l'application avec subprocess
        process = subprocess.Popen(
            [application_path, file_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Écrire les commandes
        for command in commands:
            if process.stdin:
                process.stdin.write(command + '\n')

        # Récupérer les sorties
        stdout, stderr = process.communicate()

        # S'assurer que toutes les commandes sont passées avant de fermer stdin
        if process.stdin:
            process.stdin.close()

        # Afficher les résultats
        #print("Sortie de MultiWFN:")
        #print(stdout)
        #if stderr and not stderr == "Note: The following floating-point exceptions are signalling: IEEE_INVALID_FLAG IEEE_UNDERFLOW_FLAG IEEE_DENORMAL":
        #    print("Erreurs:")
        #    print(stderr)
        print(f"Execution de {os.path.basename(file)[:-4]} terminé.")

    except Exception as e:
        print(f"Erreur lors de l'exécution de MultiWFN : {e}")

def extract_content(input_file, output_file, start_header, end_header):
    ''' Extract content between two headers in a file '''

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        if start_header in line:
            start_index = i
        if end_header in line:
            end_index = i
            break

    if start_index is None or end_index is None:
        raise ValueError("Les en-têtes spécifiés n'ont pas été trouvés dans le fichier.")

    extracted_lines = lines[start_index+1:end_index]

    with open(output_file, 'w') as outfile:
        outfile.writelines(extracted_lines)
    
    print("File saved as : "+output_file)

def creer_video(images, chemin_sortie, fps):
    """
    Crée une vidéo à partir d'une liste d'images.

    :param images: Liste des chemins des images à inclure dans la vidéo.
    :param chemin_sortie: Chemin du fichier vidéo de sortie.
    :param fps: Nombre d'images par seconde (FPS) pour la vidéo.
    """
    if not images:
        print("La liste d'images est vide.")
        return

    # Lire la première image pour obtenir les dimensions
    premiere_image = cv2.imread(images[0])
    hauteur, largeur, _ = premiere_image.shape

    # Initialiser le writer vidéo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec pour MP4
    writer = cv2.VideoWriter(chemin_sortie, fourcc, fps, (largeur, hauteur))

    for chemin_image in images:
        img = cv2.imread(chemin_image)
        if img is None:
            print(f"Erreur : Impossible de lire l'image {chemin_image}.")
            continue

        # Ajouter le nom du fichier sur l'image
        nom_image = chemin_image.split("/")[-1][:-4]  # Extraire le nom du fichier
        position = (10, hauteur - 20)  # Position du texte (x, y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        taille = 0.8
        couleur = (255, 255, 255)  # Blanc
        epaisseur = 2

        # Ajouter un fond pour rendre le texte lisible
        cv2.rectangle(img, (10, hauteur - 40), (10 + 300, hauteur - 10), (0, 0, 0), -1)

        # Ajouter le texte
        cv2.putText(img, nom_image, position, font, taille, couleur, epaisseur)

        # Ajouter l'image modifiée à la vidéo
        writer.write(img)

    # Libérer les ressources
    writer.release()
    print(f"Vidéo créée avec succès : {chemin_sortie}")

## Paramètres

# Liste des valeurs de champ électrique à étudier
ef_values = np.linspace(0.04, 0.06, 10)
ef_values_prev = "0.04 0.06 10"

# En-têtes pour extraire les fichiers .wfn
start_header = "----- TOP OF INPUT FILE FOR BADER'S AIMPAC PROGRAM -----"
end_header = "----- END OF INPUT FILE FOR BADER'S AIMPAC PROGRAM -----"

# Liste des fichiers .wfn à traiter
base_path = os.getcwd()
file0 = os.path.join(base_path, f"E0.000000/4nitroaniline_E0.000000_orca.gbw")
files = [file0]+[os.path.join(base_path, f"E{efield:.6f}/4nitroaniline_E{efield:.6f}.gbw") for i,efield in enumerate(ef_values, start=1)]

# Commandes pour extraire le champs électrique
command_efield = ['4','12','7','80,80','1','0','1','1','3','11','13','0','-5','q']
command_efield_diff = ['4','0','1',f'-,{file0}','12','7','80,80','1','0','1','1','3','11','13','0','-5','q']
command_densite = ['4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']
command_densite_pi = ['100','22','0','2','0','4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']
command_densite_sig = ['100','22','0','1','0','4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']
command_densite_sig_pinval = ['100','22','0','3','0','4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']
command_densite_pival = ['100','22','0','4','0','4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']

# Nombre d'images par seconde
fps = 1



header = ['############################################################################################################',
        '############################################################################################################',
        '##                                                                                                        ##',
        '##                                                                                                        ##',
        '##                                        Dipolar Momentum Study                                          ##',
        '##                                                                                                        ##',
        '##                                                                                                        ##',
        '############################################################################################################',
        '############################################################################################################']

command_input_text = "Types de calcul disponibles : \n 1. Calcul du champs électrique \n 2. Calcul de la variation du champs électrique \n 3. Calcul de la densité électronique pi \n 4. Calcul de la densité électronique sigma \n 5. Calcul de la densité électronique sigma sans pi de valence \n 6. Calcul de la densité électronique avec pi de valence \n 7. Etude de population \n 8. Etude de population (Fichiers orbcomp déjà présents) \n 9. Etude de la valeur d'une orbital \n 10. Calcul de la densité électronique \n 11. Extraction des énergies \nPour terminer le programme, entrez 'q' \n \n Indiquez le type de calcul que vous voulez effectuer : "

if __name__ == "__main__":
    os.system('clear')
    for line in header:
        print(line)

    print('\n\n')
    pursue = input("Voulez-vous continuer ? (y/n) : ")
    if pursue == 'n':
        exit()
    
    print('\n\n')
    os.system('sleep 1')
    ef_values = input(f"Entrez les valeurs de champ électrique min, max et le nombre de valeurs à étudier (séparés par des espaces) \n les valeurs précédentes sont ({ef_values_prev}), si vous souhaitez les utiliser tapez entrer : ")
    if ef_values == "":
        ef_values = ef_values_prev
    ef_min, ef_max, n_val = ef_values.split()
    ef_values = np.linspace(float(ef_min), float(ef_max), int(n_val))
    os.system('sleep 1')
    print(f'\n Vous avez choisi les valeurs de champ électrique suivantes : {ef_values}')
    
    file0 = os.path.join(base_path, f"E0.000000/4nitroaniline_E0.000000_orca.gbw")
    if 0.000000 in ef_values:
        files = [os.path.join(base_path, f"E{efield:.6f}/4nitroaniline_E{efield:.6f}_orca.gbw") for i,efield in enumerate(ef_values, start=1)]
    else:
        files = [file0]+[os.path.join(base_path, f"E{efield:.6f}/4nitroaniline_E{efield:.6f}_orca.gbw") for i,efield in enumerate(ef_values, start=1)]

    # Boucle pour choisir le type de calcul à effectuer
    end = False
    
    while not end :
        print('\n\n')
        os.system('sleep 1')
        command_input = input(command_input_text)
    
        if command_input == '1':
            # Définition de la commande
            command_efield = ['4','12','7','80,80','1','0','1','1','3','11','13','0','-5','q']

            # Dossier contenant les images
            dossier_images = base_path + "/Img_Results_Efield"
            if not os.path.exists(dossier_images):
                os.makedirs(dossier_images)

            # Générer la liste des chemins des images
            images = [os.path.join(dossier_images, f"{os.path.basename(file)[:-4]}.png") for file in files]

            # Chemin de la vidéo de sortie
            chemin_sortie = base_path + "/Dipolar_momentum_study_efield.mp4"

            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement du champ électrique...")
            print('\n')
            os.system('sleep 1')

            # Affichage pour vérifier
            for file in files:
                print(file)

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)

            ## Traitement des fichiers .wfn
            for file in files:
                print('\n')
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, command_efield)
                os.system(f'mv dislin.png {os.path.basename(file)[:-4]}.png')
                os.system(f'mv {os.path.basename(file)[:-4]}.png {dossier_images}')

            ## Création de la vidéo
            creer_video(images, chemin_sortie, fps)
        
        elif command_input == '2':
            # Définition de la commande
            command_efield_diff = ['4','0','1',f'-,{file0}','12','7','80,80','1','0','1','1','3','11','13','0','-5','q']

            # Dossier contenant les images
            dossier_images = base_path + "/Img_Results_Efield_diff"
            if not os.path.exists(dossier_images):
                os.makedirs(dossier_images)

            # Générer la liste des chemins des images
            images = [os.path.join(dossier_images, f"{os.path.basename(file)[:-4]}.png") for file in files]

            # Chemin de la vidéo de sortie
            chemin_sortie = base_path + "/Dipolar_momentum_study_efield_diff.mp4"

            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement de la variation du champ électrique...")
            print('\n')
            os.system('sleep 1')

            # Affichage pour vérifier
            for file in files:
                print(file)

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)

            ## Traitement des fichiers .wfn
            for file in files:
                print('\n')
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, command_efield_diff)
                os.system(f'mv dislin.png {os.path.basename(file)[:-4]}.png')
                os.system(f'mv {os.path.basename(file)[:-4]}.png {dossier_images}')

            ## Création de la vidéo
            creer_video(images, chemin_sortie, fps)

        elif command_input == '3':
            # Creation file0_pi
            file0 = os.path.join(base_path, f"4nitroaniline_E0.000000_pi.wfn")
            command_file0_pi = ['100','22','0','2','2','5',f'{file0}','q']

            # Définition de la commande
            command_densite_pi = ['100','22','0','2','0','4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']

            # Dossier contenant les images
            dossier_images = base_path + "/Img_Results_Diff_density_pi"
            if not os.path.exists(dossier_images):
                os.makedirs(dossier_images)

            # Générer la liste des chemins des images
            images = [os.path.join(dossier_images, f"{os.path.basename(file)[:-4]}.png") for file in files]

            # Chemin de la vidéo de sortie
            chemin_sortie = base_path + "/Dipolar_momentum_study_diff_density_pi.mp4"

            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement de la densité électronique pi...")
            print('\n')
            os.system('sleep 1')

            # Affichage pour vérifier
            for file in files:
                print(file)

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)

            ## Traitement des fichiers .wfn
            for file in files:
                print('\n')
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, command_densite_pi)
                os.system(f'mv dislin.png {os.path.basename(file)[:-4]}.png')
                os.system(f'mv {os.path.basename(file)[:-4]}.png {dossier_images}')

            ## Création de la vidéo
            creer_video(images, chemin_sortie, fps)

        elif command_input == '4':
            # Creation file0_sig
            file0 = os.path.join(base_path, f"4nitroaniline_E0.000000_sig.wfn")
            command_file0_sig = ['100','22','0','1','2','5',f'{file0}','q']

            # Définition de la commande
            command_densite_sig = ['100','22','0','1','0','4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']

            # Dossier contenant les images
            dossier_images = base_path + "/Img_Results_Diff_density_sig"
            if not os.path.exists(dossier_images):
                os.makedirs(dossier_images)

            # Générer la liste des chemins des images
            images = [os.path.join(dossier_images, f"{os.path.basename(file)[:-4]}.png") for file in files]

            # Chemin de la vidéo de sortie
            chemin_sortie = base_path + "/Dipolar_momentum_study_diff_density_sig.mp4"

            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement de la densité électronique sigma...")
            print('\n')
            os.system('sleep 1')

            # Affichage pour vérifier
            for file in files:
                print(file)

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)

            ## Traitement des fichiers .wfn
            for file in files:
                print('\n')
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, command_densite_sig)
                os.system(f'mv dislin.png {os.path.basename(file)[:-4]}.png')
                os.system(f'mv {os.path.basename(file)[:-4]}.png {dossier_images}')

            ## Création de la vidéo
            creer_video(images, chemin_sortie, fps)
        
        elif command_input == '5':
            # Creation file0_sig_pinval
            file0 = os.path.join(base_path, f"4nitroaniline_E0.000000_sig_pinval.wfn")
            command_file0_sig_pinval = ['100','22','0','3','2','5',f'{file0}','q']

            # Définition de la commande
            command_densite_sig_pinval = ['100','22','0','3','0','4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']

            # Dossier contenant les images
            dossier_images = base_path + "/Img_Results_Diff_density_sig_pinval"
            if not os.path.exists(dossier_images):
                os.makedirs(dossier_images)

            # Générer la liste des chemins des images
            images = [os.path.join(dossier_images, f"{os.path.basename(file)[:-4]}.png") for file in files]

            # Chemin de la vidéo de sortie
            chemin_sortie = base_path + "/Dipolar_momentum_study_diff_density_sig_pinval.mp4"

            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement de la densité électronique sigma sans pi de valence...")
            print('\n')
            os.system('sleep 1')

            # Affichage pour vérifier
            for file in files:
                print(file)

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)

            ## Traitement des fichiers .wfn
            for file in files:
                print('\n')
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, command_densite_sig_pinval)
                os.system(f'mv dislin.png {os.path.basename(file)[:-4]}.png')
                os.system(f'mv {os.path.basename(file)[:-4]}.png {dossier_images}')

            ## Création de la vidéo
            creer_video(images, chemin_sortie, fps)

        elif command_input == '6':
            # Creation file0_pival
            file0 = os.path.join(base_path, f"4nitroaniline_E0.000000_pival.wfn")
            command_file0_sig = ['100','22','0','4','2','5',f'{file0}','q']

            # Définition de la commande
            command_densite_pival = ['100','22','0','4','0','4','0','1',f'-,{file0}','1','1','200,200','1','0.2','19','8','1','-0.1,0.1','4','5','0','-5','q']

            # Dossier contenant les images
            dossier_images = base_path + "/Img_Results_Diff_density_pival"
            if not os.path.exists(dossier_images):
                os.makedirs(dossier_images)

            # Générer la liste des chemins des images
            images = [os.path.join(dossier_images, f"{os.path.basename(file)[:-4]}.png") for file in files]

            # Chemin de la vidéo de sortie
            chemin_sortie = base_path + "/Dipolar_momentum_study_diff_density_pival.mp4"

            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement de la densité électronique pi de valence...")
            print('\n')
            os.system('sleep 1')

            # Affichage pour vérifier
            for file in files:
                print(file)

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)

            ## Traitement des fichiers .wfn
            for file in files:
                print('\n')
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, command_densite_pival)
                os.system(f'mv dislin.png {os.path.basename(file)[:-4]}.png')
                os.system(f'mv {os.path.basename(file)[:-4]}.png {dossier_images}')

            ## Création de la vidéo
            creer_video(images, chemin_sortie, fps)

        elif command_input == '7':
            # Définition de la commande
            command_pop = ['8','8','1','-4','0','-10','q']

            # Dossier contenant les obrcomp.txt
            dossier_orbcomp = base_path + "/Txt_Results_orbcomp"
            if not os.path.exists(dossier_orbcomp):
                os.makedirs(dossier_orbcomp)

            # Générer la liste des chemins des orbcomp.txt
            orbcomp = [os.path.join(dossier_orbcomp, f"{os.path.basename(file)[:-4]}_orbcomp.txt") for file in files]

            print('\n\n')
            os.system('sleep 1')
            print("Début de l'étude de population...")
            print('\n')
            os.system('sleep 1')

            # Affichage pour vérifier
            for file in files:
                print(file)

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)

            ## Traitement des fichiers .wfn
            for file in files:
                print('\n')
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, command_pop)
                os.system(f'mv orbcomp.txt {os.path.basename(file)[:-4]}_orbcomp.txt')
                os.system(f'mv {os.path.basename(file)[:-4]}_orbcomp.txt {dossier_orbcomp}')

            ## Traitement des fichiers orbcomp.txt
            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement des fichiers orbcomp.txt...")
            print('\n')
            os.system('sleep 1')

            orbcomp_table = np.zeros((len(orbcomp), 262, 16)) # Tableau contenant les données des orbcomp.txt
            x = 0

            for file in orbcomp:
                print('\n')
                print(f"Traitement de {file}...")
                with open(file, 'r') as infile:
                    lines = infile.readlines()
                    y, z = -1, 0
                    for line in lines:
                        if 'Orbital' in line:
                            z = 0
                            y += 1
                        elif '%' in line:
                            orbcomp_table[x,y,z] = float(line.split()[-2])
                            z += 1
                x += 1
            
            print('\n\n')
            os.system('sleep 1')
            orbital = input("Entrez le numéro de l'orbital à étudier : ")
            print('\n\n')
            os.system('sleep 1')
            print(f"Orbital {orbital} :")
            print('\n')
            os.system('sleep 1')
            
            plt.figure()
            for i in range(16):
                plt.plot(ef_values, orbcomp_table[1:,int(orbital)-1, i], marker='o', linestyle='-', label=f"Atome {i+1}")
            plt.xlabel("Electric Field E0 (a.u.)")
            plt.ylabel("Population (en %)")
            plt.title(f"Population de l'orbital {orbital} vs. Electric Field")
            plt.legend()
            plt.grid()
            plt.savefig(dpi=300, fname="population_vs_efield.png")
            print("Graphique sauvegardé sous le nom de population_vs_efield.png")

        elif command_input == '8':
            # Dossier contenant les obrcomp.txt
            dossier_orbcomp = base_path + "/Txt_Results_orbcomp"

            # Générer la liste des chemins des orbcomp.txt
            orbcomp = [os.path.join(dossier_orbcomp, f"{os.path.basename(file)[:-4]}_orbcomp.txt") for file in files]

            ## Traitement des fichiers orbcomp.txt
            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement des fichiers orbcomp.txt...")
            print('\n')
            os.system('sleep 1')

            orbcomp_table = np.zeros((len(orbcomp), 262, 16)) # Tableau contenant les données des orbcomp.txt
            x = 0

            for file in orbcomp:
                print('\n')
                print(f"Traitement de {file}...")
                with open(file, 'r') as infile:
                    lines = infile.readlines()
                    y, z = -1, 0
                    for line in lines:
                        if 'Orbital' in line:
                            z = 0
                            y += 1
                        elif '%' in line:
                            orbcomp_table[x,y,z] = float(line.split()[-2])
                            z += 1
                x += 1
            
            print('\n\n')
            os.system('sleep 1')
            atom_orb = input("Etude de population en fonction des atomes ou des orbitales (a,o) : ")
            print('\n\n')
            os.system('sleep 1')

            if atom_orb == "a":
                print('Etude de population en fonction des atomes')
                print('\n')
                os.system('sleep 1')

                print('\n\n')
                os.system('sleep 1')
                orbital = input("Entrez le numéro de l'orbital à étudier : ")
                print('\n\n')
                os.system('sleep 1')
                print(f"Etude de l'orbital {orbital} :")
                print('\n')
                os.system('sleep 1')

                atoms = input("Entrez les atomes à étudier \n (vous pouvez les entrer à la suite séparés par des virgules \n ou bien choisir une suite d'atome avec un tiret : 4-8) : ")
                atoms = atoms.split(',')
                atoms_list = []
                for atom in atoms:
                    if '-' in atom:
                        start, end = atom.split('-')
                        atoms_list += list(range(int(start), int(end)+1))
                    else:
                        atoms_list.append(int(atom))
                print('\n\n')
                os.system('sleep 1')
                print(f"Etude de l'orbital {orbital} et des atomes {atoms_list}:")
                print('\n')
                os.system('sleep 1')
                
                plt.figure()
                for i in atoms_list:
                    plt.plot(ef_values, orbcomp_table[1:,int(orbital)-1, i-1], marker='o', linestyle='-', label=f"Atome {i}")
                plt.xlabel("Electric Field E0 (a.u.)")
                plt.ylabel("Population (en %)")
                plt.title(f"Population de l'orbital {orbital} vs. Electric Field")
                plt.legend()
                plt.grid()
                plt.savefig(dpi=300, fname=f"population_vs_efield{atoms}.png")
                print("Graphique sauvegardé sous le nom de population_vs_efield.png")
            
            elif atom_orb == "o":
                print('Etude de population en fonction des orbitales')
                print('\n')
                os.system('sleep 1')

                print('\n\n')
                os.system('sleep 1')
                atome = input("Entrez le numéro de l'atome à étudier : ")
                print('\n\n')
                os.system('sleep 1')
                print(f"Etude de l'atome {atome} :")
                print('\n')
                os.system('sleep 1')

                orbitales = input("Entrez les orbitales à étudier \n (vous pouvez les entrer à la suite séparés par des virgules \n ou bien choisir une suite d'orbitales avec un tiret : 4-8) : ")
                orbitales = orbitales.split(',')
                orb_list = []
                for orbital in orbitales:
                    if '-' in orbital:
                        start, end = orbital.split('-')
                        orb_list += list(range(int(start), int(end)+1))
                    else:
                        orb_list.append(int(orbital))
                print('\n\n')
                os.system('sleep 1')
                print(f"Etude de l'atome {atome} et des orbitales {orb_list}:")
                print('\n')
                os.system('sleep 1')

                plt.figure()
                orb_max = 0
                max_var = 0
                for i in orb_list:
                    if orbcomp_table[1,i-1, int(atome)-1] == 0.0:
                        print(f"L'orbital {i} de l'atome {atome} n'est pas peuplé.")
                        var = orbcomp_table[1:,i-1, int(atome)-1]
                    else:
                        var = 100*(orbcomp_table[1:,i-1, int(atome)-1]-orbcomp_table[1,i-1, int(atome)-1])/orbcomp_table[1,i-1, int(atome)-1]
                    if max(var) > max_var:
                        orb_max = i
                        max_var = max(var)
                    plt.plot(ef_values, var, marker='o', linestyle='-', label=f"Orbital {i}")
                plt.xlabel("Electric Field E0 (a.u.)")
                plt.ylabel("Variation de population (en %)")
                plt.title(f"Population de l'orbital {orbital} vs. Electric Field")
                plt.legend()
                plt.grid()
                plt.savefig(dpi=300, fname=f"population_vs_efield_{int(atome)}.png")
                print('\n')
                print(f"L'orbital de variation max est : {orb_max} \n")
                print(f"Graphique sauvegardé sous le nom de population_vs_efield_{int(atome)}.png")
            
        elif command_input == '9':

            os.system('sleep 1')
            print("Etude du champ électrique pour une orbitale donnée.")
            print('\n')
            os.system('sleep 1')
            orbs = input("Entrez les numéros des orbitals à étudier (ex: 1,4-7 -> 1,4,5,6,7): ")
            orbitales = orbs.split(',')
            orbs_list = []
            for orb in orbitales:
                if '-' in orb:
                    start, end = orb.split('-')
                    orbs_list += list(range(int(start), int(end)+1))
                else:
                    orbs_list.append(int(orb))
            print('\n\n')
            os.system('sleep 1')

            diff_input = input("Faire la différence avec absence du champs (y,n) : ")
            print('\n\n')
            os.system('sleep 1')

            # Dossier contenant les images
            dossier_images = base_path + "/Img_Results_Efield_orb"
            if not os.path.exists(dossier_images):
                os.makedirs(dossier_images)

            for orbital in orbs_list:
                # Définition de la commande
                if diff_input == "y":
                    command_efield = ['5','0','1',f'-,{file0}','4',f'{orbital}','2',f'{orbital}','1','0','q']
                else :
                    command_efield = ['5','4',f'{orbital}','2','1','0','q']

                # Générer la liste des chemins des images
                images = [os.path.join(dossier_images, f"{os.path.basename(file)[:-4]}_{orbital}.png") for file in files]

                # Chemin de la vidéo de sortie
                chemin_sortie = base_path + f"/Dipolar_momentum_study_efield_orb_{orbital}.mp4"

                print('\n\n')
                os.system('sleep 1')
                print(f"Début du traitement de l'orbital {orbital}...")
                print('\n')
                os.system('sleep 1')

                # Affichage pour vérifier
                for file in files:
                    print(file)

                ## Extraction des fichiers .wfn
                #for i in range(len(files)):
                #    if not os.path.exists(files[i]):
                #        input_file = files[i][:-3]+'dat'
                #        output_file = input_file
                #        extract_content(input_file, output_file, start_header, end_header)

                ## Traitement des fichiers .wfn
                for file in files:
                    print('\n')
                    print(f"Traitement de {file}...")
                    MultiWFN_exe(file, command_efield)
                    os.system(f'mv dislin.png {os.path.basename(file)[:-4]}_{orbital}.png')
                    os.system(f'mv {os.path.basename(file)[:-4]}_{orbital}.png {dossier_images}')

                ## Création de la vidéo
                creer_video(images, chemin_sortie, fps)

        elif command_input == '10':
            # Dossier contenant les images
            dossier_images = base_path + "/Img_Results_density_diff"
            if not os.path.exists(dossier_images):
                os.makedirs(dossier_images)

            # Générer la liste des chemins des images
            images = [os.path.join(dossier_images, f"{os.path.basename(file)[:-4]}.png") for file in files]

            # Chemin de la vidéo de sortie
            chemin_sortie = base_path + "/Dipolar_momentum_study_density_diff.mp4"

            print('\n\n')
            os.system('sleep 1')
            print("Début du traitement de la variation de densité...")
            print('\n')
            os.system('sleep 1')

            # Affichage pour vérifier
            for file in files:
                print(file)

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)

            ## Traitement des fichiers .wfn
            for file in files:
                print('\n')
                print(f"Traitement de {file}...")
                MultiWFN_exe(file, command_densite)
                os.system(f'mv dislin.png {os.path.basename(file)[:-4]}.png')
                os.system(f'mv {os.path.basename(file)[:-4]}.png {dossier_images}')

            ## Création de la vidéo
            creer_video(images, chemin_sortie, fps)

        elif command_input == '11':
            # Chemin de la vidéo de sortie
            chemin_sortie_energy = base_path + "/energy_vs_efield.png"
            chemin_sortie_dipole = base_path + "/dipole_vs_efield.png"

            print('\n\n')
            os.system('sleep 1')
            print("Début de l'extraction des énergies...")
            print('\n')
            os.system('sleep 1')

            mol_properties_txt = [file[:-3]+"property.txt" for file in files]

            # Affichage pour vérifier
            for file in files:
                print(file)

            properties = np.zeros((len(mol_properties_txt), 2))
            for i in range(len(mol_properties_txt)):
                print('\n')
                print(f"Traitement de {mol_properties_txt[i]}...")
                with open(mol_properties_txt[i], 'r') as infile:
                    lines = infile.readlines()
                    for line in lines:
                        if '&TOTALENERGY [&Type "Double"]' in line:
                            properties[i,0] = float(line.split()[-2])
                        elif '&DIPOLEMAGNITUDE' in line:
                            properties[i,1] = float(line.split()[-1])

            print('\n')
            print("Traitements terminés.")
            print('\n')
            os.system('sleep 1')

            print('\n')
            save_prop = input("Voulez-vous sauvegarder les données ? (y/n) : ")

            if save_prop == 'y':
                print('\n')
                os.system('sleep 1')
                print("Sauvegarde des données...")
                print('\n')
                os.system('sleep 1')

                np.savetxt(base_path + "/dipole_moments_energy_vs_efield.txt", np.column_stack((ef_values,properties[1:,0],properties[1:,1])), delimiter='\t', header="Electric Field\tTotal Energy\tDipole Magnitude", comments='')
                print(f"Données sauvegardées sous le nom de dipole_moments_energy_vs_efield.txt")

            if 0.000000 not in ef_values:
                properties = properties[1:]

            plt.figure()
            plt.plot(ef_values, properties[:,0], marker='o', linestyle='-', label="Energie totale")
            plt.xlabel("Electric Field E0 (a.u.)")
            plt.ylabel("Energie (en a.u.)")
            plt.title("Energie totale vs. Electric Field")
            plt.legend()
            plt.grid()
            plt.savefig(dpi=300, fname="energy_vs_efield.png")
            print(f"Graphique sauvegardé sous le nom de {os.path.basename(chemin_sortie_energy)}")

            plt.figure()
            plt.plot(ef_values, properties[:,1], marker='o', linestyle='-', label="Dipole Magnitude")
            plt.xlabel("Electric Field E0 (a.u.)")
            plt.ylabel("Dipole Magnitude (en a.u.)")
            plt.title("Dipole Magnitude vs. Electric Field")
            plt.legend()
            plt.grid()
            plt.savefig(dpi=300, fname="dipole_vs_efield.png")
            print(f"Graphique sauvegardé sous le nom de {os.path.basename(chemin_sortie_dipole)}")

            ## Extraction des fichiers .wfn
            #for i in range(len(files)):
            #    if not os.path.exists(files[i]):
            #        input_file = files[i][:-3]+'dat'
            #        output_file = input_file
            #        extract_content(input_file, output_file, start_header, end_header)



        elif command_input == 'q':
            end = True
            print("Fin du programme.")

        else:
            print("Commande non reconnue, veuillez réessayer.")