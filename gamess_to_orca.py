import numpy as np
import os
from tkinter import *
import tkinter.filedialog

def traiter_fichier_inp(fichier_entree, fichier_sortie, entete, dossier_sortie):
    """
    Lit un fichier .inp, extrait les lignes entre 'C1' et '$END',
    retire la deuxième colonne si elle existe, et écrit le résultat dans un nouveau fichier .inp avec une en-tête.

    :param fichier_entree: Chemin vers le fichier .inp d'entrée.
    :param fichier_sortie: Chemin vers le fichier .inp de sortie.
    :param entete: Texte à ajouter comme en-tête dans le fichier de sortie.
    """
    try:
        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(dossier_sortie, exist_ok=True)

        # Chemin complet pour le fichier de sortie
        chemin_fichier_sortie = os.path.join(dossier_sortie, fichier_sortie)

        # Lire toutes les lignes du fichier d'entrée
        with open(fichier_entree, 'r', encoding='utf-8') as entree:
            lignes = entree.readlines()

        # Identifier les indices des marqueurs 'C1' et '$END'
        indice_debut = next(i for i, ligne in enumerate(lignes) if 'C1\n' in ligne)
        indice_fin = next(i for i, ligne in enumerate(lignes[indice_debut:]) if ' $END' in ligne)+indice_debut

        # Extraire les lignes entre 'C1' et '$END' (exclusives)
        partie_interessante = lignes[indice_debut + 1:indice_fin]

        # Vérifier si la partie intéressante contient des données
        if not partie_interessante:
            raise ValueError("Aucune donnée trouvée entre les marqueurs 'C1\n' et ' $END'.")

        # Convertir la partie intéressante en tableau NumPy ligne par ligne
        data = []
        for ligne in partie_interessante:
            if ligne.strip():  # Ignorer les lignes vides
                data.append(ligne.split())

        # Vérifier si des données valides ont été trouvées
        if not data:
            raise ValueError("Les lignes entre 'C1' et '$END' ne contiennent pas de données valides.")

        # Convertir la liste en tableau NumPy
        data = np.array(data)

        # Supprimer la deuxième colonne si elle existe
        if data.shape[1] > 1:
            data_sans_col2 = np.delete(data, 1, axis=1)
        else:
            data_sans_col2 = data  # Pas de deuxième colonne à supprimer

        # Écrire l'en-tête et les données dans le fichier de sortie
        with open(chemin_fichier_sortie, 'w', encoding='utf-8') as sortie:
            sortie.write(entete)  # Ajouter l'en-tête
            for ligne in data_sans_col2:
                sortie.write("    ".join(ligne) + "\n")  # Formater les données ligne par ligne
            sortie.write("*")  # Réinsérer le marqueur de fin

        print(f"Fichier '{chemin_fichier_sortie}' créé avec succès.")

    except StopIteration:
        print("Impossible de trouver les marqueurs 'C1' ou '$END' dans le fichier.")
    except ValueError as ve:
        print(f"Erreur : {ve}")
    except FileNotFoundError:
        print(f"Le fichier '{fichier_entree}' est introuvable.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")

initial_dir = os.getcwd()

input_file = tkinter.filedialog.askopenfilename(initialdir=initial_dir)

output_file = input_file.replace(".inp", "_orca.inp")

chemin_fichiers_sortie = os.getcwd()

print(input_file)
entete = """\
# Advanced Mode
# 
! B3LYP OPT 6-311G(d,p) NormalPrint NormalSCF 
%scf
	MaxIter 125
	CNVDIIS 1
	CNVSOSCF 1 
end
%output
	print[p_mos] true
	print[p_basis] 5
end

%MaxCore 4000

* xyz 0 1
"""

traiter_fichier_inp(input_file, output_file, entete, chemin_fichiers_sortie)
