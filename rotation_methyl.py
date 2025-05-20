#i want to change the coordinates of the methyl hydrogens in the aspirin and rotate then around the carbon axis in the dat file 

import os   
import numpy as np  
import pandas as pd
import re   
from pathlib import Path    
import subprocess   
import time   
import pyautogui              
from PIL import ImageGrab           

# Define base directories            
BASE_DIR = Path(r"C:\Users\Public\gamess-64") # Directory of this script
GAMESS_DIR = BASE_DIR  # Update this with your GAMESS installation path
OUTPUT_DIR = Path(r"C:\Users\Public\gamess-64\inputs")  # Directory for output files
OUTPUT_DIR.mkdir(exist_ok=True)  # Create the directory if it doesn't exist     

# Define functions            
def automation(theta,file,iteration):
    with open(file, "r") as f:
        coord = f.readlines()
    carbon = np.array([3.53050 , 0.59960  , 0.16350])
    H1 = np.array([float(i) for i in coord[-5].strip().split()[2:]])
    H2 = np.array([float(i) for i in coord[-4].strip().split()[2:]])
    H3 = np.array([float(i) for i in coord[-3].strip().split()[2:]])
      
    A, B, C = H1 - carbon, H2 - carbon, H3 - carbon
    # calculate the normal vector to the plane of the hydrogen atoms
    normal_vector = np.cross(A, B)
    normal_vector = normal_vector / np.linalg.norm(normal_vector)
    center, r = circumcircle(A, B, C)            
    vecA, vecB, vecC = A - center, B - center, C - center
    # calculate the vector perpendicular to the plane of the hydrogen atoms
    Z = np.cross(vecA, vecB) + center
    Z= Z / np.linalg.norm(Z)           
    # Rotate the hydrogen atoms around the carbon atom
    A_r = rotation_z(vecA, Z, theta) + center            
    B_r = rotation_z(vecB, Z, theta) + center            
    C_r = rotation_z(vecC, Z, theta) + center 

    H1_r = [round(num, 5) for num in A_r+carbon] 
    #H1_r = A_r+carbon      
    #H2_r = B_r+carbon      
    #H3_r = C_r+carbon      
    H2_r = [round(num, 5) for num in B_r+carbon]          
    H3_r = [round(num, 5) for num in C_r+carbon]                    
               
    # Write to input file for GAMESS                                    
    output_file = OUTPUT_DIR / f"aspirin{iteration}.inp"            
    with open(output_file, "w") as f:                
        f.write("""
 $CONTRL SCFTYP=RHF RUNTYP=ENERGY CCTYP=CCSD(T) MAXIT=50 ISPHER=1 $END
 $SYSTEM MWORDS=200 MEMDDI=20 $END
 $BASIS GBASIS=ACCT NGAUSS=3 NDFUNC=2 NFFUNC=1 DIFFSP=.TRUE. DIFFS=.TRUE. $END
 $GUESS GUESS=HUCKEL $END	
 $DATA 
Title
C1
O     8.0     1.23330     0.55400     0.77920
O     8.0    -0.69520    -2.71480    -0.75020
O     8.0     0.79580    -2.18430     0.86850
O     8.0     1.78130     0.81050    -1.48210
C     6.0    -0.08570     0.60880     0.44030
C     6.0    -0.79270    -0.55150     0.12440
C     6.0    -0.72880     1.84640     0.41330
C     6.0    -2.14260    -0.47410    -0.21840
C     6.0    -2.07870     1.92380     0.07060
C     6.0    -2.78550     0.76360    -0.24530
C     6.0    -0.14090    -1.85360     0.14770
C     6.0     2.10940     0.67150    -0.31130
C     6.0     3.53050     0.59960     0.16350
H     1.0    -0.18510     2.75450     0.65930
H     1.0    -2.72470    -1.36050    -0.45640
H     1.0    -2.57970     2.88720     0.05060
H     1.0    -3.83740     0.82380    -0.50900
H     1.0    """+str(H1_r[0])+"     "+str(H1_r[1])+"     "+str(H1_r[2])+"""
H     1.0    """+str(H2_r[0])+"     "+str(H2_r[1])+"     "+str(H2_r[2])+"""
H     1.0    """+str(H3_r[0])+"     "+str(H3_r[1])+"     "+str(H3_r[2])+"""
H     1.0    -0.25550    -3.59160    -0.73370
 $END
""")

#defining the rotation_z function            
def rotation_z(vec, Z, angle):                        
    return np.cos(angle) * vec + np.sin(angle) * np.cross(vec, Z) +(1 - np.cos(angle))* np.dot(vec, Z) * Z            
def circumcircle(A, B, C):                
    A, B, C = A / np.linalg.norm(A), B / np.linalg.norm(B), C / np.linalg.norm(C)                
    center = (A + B + C) / 3                
    r = np.linalg.norm(A - center)                
    return center, r  



for i in range(1,20):            
    automation(np.pi/30*i,r"C:\Users\Public\gamess-64\inputs\aspirin1.inp",i)
