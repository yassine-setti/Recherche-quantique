import subprocess
import pyautogui
import time
from PIL import ImageGrab
import os
import pathlib
Position={'Return':(1503,78),'up':(1494,114),'down':(1490,154),'left':(1490,193),'right':(149,226),'zoomin':(1488,265),'savepicture':(1483,377)}

def MultiWFN_exe(file_path,commands):
    #Ouvre MultiWFN
    application_path = r"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\Multiwfn.exe"
    #pathlib.Path()
    # Ouvrir l'application avec subprocess
    process = subprocess.Popen([application_path, file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)

    # Execution des actions sur l'application
    test=False
    for command in commands:

        process.stdin.write(command + '\n')
        if command=='q':
            test=True
            break
    if test:
        process.stdin.write('y\n')
    process.stdin.close()

    # Attendre que le processus se termine
    stdout, stderr = process.communicate()

    # Afficher la sortie de Multiwfn
    print("Sortie de Multiwfn:")
    print(stdout)
    
    # S'il y a des erreurs, les afficher
    if stderr:
        print("Erreurs:")
        print(stderr)





# Liste des fichiers .wfn à traiter 
#files = ['D:\\Users\\Hugo\\SynologyDrive\\CentraleSupelec\\2A\\Cours\\ProjetENTRAVE\\FichierWFNaspirine\\aspirin2.wfn', 'D:\\Users\\Hugo\\SynologyDrive\\CentraleSupelec\\2A\\Cours\\ProjetENTRAVE\\FichierWFNaspirine\\aspirin3.wfn','D:\\Users\\Hugo\\SynologyDrive\\CentraleSupelec\\2A\\Cours\\ProjetENTRAVE\\FichierWFNaspirine\\aspirin4.wfn','D:\\Users\\Hugo\\SynologyDrive\\CentraleSupelec\\2A\\Cours\\ProjetENTRAVE\\FichierWFNaspirine\\aspirin5.wfn']


files = []

base_path = r"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files"
file_prefix = 'aniline'
file_extension = '.wfn'

# Boucle pour générer les chemins des fichiers de 1 à 40
for i in range(1, 50):
    file_name = f"{file_prefix}{i}{file_extension}"
    full_path = f"{base_path}\\{file_name}"
    files.append(full_path)

# Affichage pour vérifier
for file in files:
    print(file)
# Commandes à exécuter pour chaque fichier dans Multiwfn

### ATTENTION le screen se fait en sauvegardant depuis les commandes la figure


from keyboard import press  

os.chdir(r"C:\Users\yassi\Desktop\2A\Recherche\Scripts")

commands_elf=['4','10','2','200,200','4','1,6,7','1','6','8','1','0']
commands_orbitales=['5','4','35','3','4','0.02','1']
commands_LOL=['4','10','2','200,200','4','1,12,13','1','6','8','1','3','0','8','0,0.01,20','y','1','0']
commands_fukui=['22', '3', '3', '1']
valeur='0'
def lancer_screens(commands):
    for file in files:
        print(f"Traitement de {file}...")
        MultiWFN_exe(file, [file]+commands)
        print(f"{file} terminé.\n")
        time.sleep(1)
    
lancer_screens(commands_orbitales)


