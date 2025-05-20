
import subprocess
import pyautogui
import time
from PIL import ImageGrab
import os
import pathlib
import pyperclip
import matplotlib.pyplot as plt

def MultiWFN_exe(file_path,commands):
    #Ouvre MultiWFN
    application_path = r"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\Multiwfn.exe"
    #pathlib.Path()

    # Ouvrir l'application avec subprocess
    process = subprocess.Popen([application_path, file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)


    # Execution des actions sur l'application
    test=False
    for command in commands:
        if command=='click':
            pyautogui.click(900,517)
            continue
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
    return stdout





# Liste des fichiers .wfn à traiter 


files = []

base_path = r"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files"
file_prefix = '4nitroaniline'
file_extension = '.wfn'

# Boucle pour générer les chemins des fichiers de 1 à 40
for i in range(1,50):
    file_name = f"{file_prefix}{i}{file_extension}"
    full_path = f"{base_path}\{file_name}"
    files.append(full_path)

# Affichage pour vérifier
for file in files:
    print(file)


# Commandes à exécuter pour chaque fichier dans Multiwfn
commands=['6','3']

d={}
Y=[]
for file in files:
    d[file]={}
    result=MultiWFN_exe(file, [file]+commands)     #Ouvre MultiWFN 
    time.sleep(2) #Attendre 1 seconde   
    pyperclip.copy(result)

    text=pyperclip.paste()
    if "             ============ Modify & Check wavefunction ============ " not in text:
        continue
    text=text.split("\n")
    print(text)
    m=text.index("             ============ Modify & Check wavefunction ============ ")
    text=text[m+1:]
    m=text.index("             ============ Modify & Check wavefunction ============ ")
    n=text.index(" Basic information of all orbitals:")
    #Leave the multiwfn terminal
    time.sleep(1) #Attendre 1 seconde 
    text=text[n+1:m-1]     
    for orb in text:
        L=orb.split()
        n,energy,=L[1],L[4]
        d[file][n]=energy

#save the dictionary d in a text file                                               
with open("d.txt", "w") as f:
    f.write(str(d))     


print(d[rf"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files\4nitroaniline{23}.wfn"])
print(d[rf"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files\4nitroaniline{25}.wfn"])
#files 23 and 25 are empty

X=[i for i in range(2,50)]
for n in range(28,37):
    X=[i for i in range(2,49)]
    for i in range(2,49):
        if str(n) not in d[rf"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files\4nitroaniline{i}.wfn"]:
            print(i)
            
    Y=[float(d[rf"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files\4nitroaniline{i}.wfn"][str(n)])  if str(n) in d[rf"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\wfn_files\4nitroaniline{i}.wfn"] else None for i in range(2,49)]
    plt.plot(X,Y,label=f"Orbital {n}")
#plt.legend()
plt.show()
          

    