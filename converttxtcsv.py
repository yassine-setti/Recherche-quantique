import pandas as pd
import numpy as np
import os

path= 'D:\\Users\\Hugo\\SynologyDrive\\CentraleSupelec\\2A/Cours\\ProjetENTRAVE\\Densiteelectronique'


for i in range(6):
# Concaténer les parties du chemin
    file_path = os.path.join(path, f'data{i}.txt')
    output_path = os.path.join(path, f'rotation{i}.csv')
# Charge les data et délimite selon les différentes colonnes du .csv
    data = pd.read_csv(file_path, delim_whitespace=True, header=None)
    x=data[0]
    y=data[1]
    z=data[2]
# Enregistre en tant que .CSV
    data.to_csv(output_path, index=False, header=False)

# Initialiser une liste pour stocker les colonnes à soustraire
columns = []

# Boucle pour charger les fichiers et extraire la 6e colonne
for i in range(6):
    # Charger le fichier CSV correspondant
    file_path = os.path.join(path, f'rotation{i}.csv')
    
    # Lire le fichier CSV
    data = pd.read_csv(file_path, header=None)
    
    # Extraire la 6e colonne (index 5)
    columns.append(data[5])

# Effectuer les soustractions entre les colonnes
# Exemple : soustraction entre la première et la deuxième colonne
soustract=[]
for i in range (5):
    soustract.append(columns[i+1]-columns[0])



######################################## calcul du vecteur unitaire normal au plan ####################

v1=np.array([x[0]-x[10],y[0]-y[10],z[0]-z[10]])
v2=np.array([x[1]-x[20],y[1]-y[20],z[1]-z[20]])

n=np.cross(v1,v2)
n=n/np.linalg.norm(n)


import matplotlib.pyplot as plt


Max=[]
# Début du plot des densités électroniques 
for i in range(5):
    P = []  # Liste pour les points positifs
    N = []  # Liste pour les points négatifs
    Z = []  # Liste pour les points nuls
    
    # Les colonnes `x` et `y` doivent déjà être définies (par exemple en lisant les fichiers CSV)
    # Assumons que `x` et `y` soient définis et ont la même longueur que `soustract[i]`

    for j in range(len(soustract[i])):
        if soustract[i][j] > 0.5:
            P.append([x[j]+n[0]*soustract[i][j], y[j]+n[1]*soustract[i][j],z[j]+n[2]*soustract[i][j]])
        elif soustract[i][j] < -0.5:
            N.append([x[j]+n[0]*soustract[i][j], y[j]+n[1]*soustract[i][j],z[j]+n[2]*soustract[i][j]])
        else:
            Z.append([x[j]+n[0]*soustract[i][j], y[j]+n[1]*soustract[i][j],z[j]+n[2]*soustract[i][j]])


    # Convertir les listes P, N, Z en trois listes séparées pour x, y et z
    if P:
        P = list(zip(*P))  # Décompresse les points positifs en 3 listes : P[0] = x, P[1] = y, P[2] = z
    if N:
        N = list(zip(*N))  # Décompresse les points négatifs en 3 listes
    if Z:
        Z = list(zip(*Z))  # Décompresse les points nuls (si nécessaire)

    # Créer la figure 3D
    fig = plt.figure(i)
    ax = fig.add_subplot(111, projection='3d')

    # Tracer les points positifs en rouge
    if P:
        ax.plot3D(P[0], P[1], P[2], 'red', label='Positive Density')
        Max.append((P[0][np.argmax(P[2])],P[1][np.argmax(P[2])]))


    
    # Tracer les points négatifs en bleu
    if N:
        ax.plot3D(N[0], N[1], N[2], 'blue', label='Negative Density')
        Max.append((N[0][np.argmin(N[2])],N[1][np.argmin(N[2])]))

    # Ajouter des labels et une légende
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Density')
    ax.legend()


file_path = os.path.join(path, 'atom_positions.csv')
data=pd.read_csv(file_path, delim_whitespace=True, header=None)
symb=data[0]
x=data[1]
y=data[2]
z=data[3]
ax.scatter(x, y, z, s=100, c='b', alpha=0.6)

# Afficher les graphes
plt.show()

print(Max)