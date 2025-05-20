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
    azote = np.array([2.31980,0.00000,0.00060])
    H1 = np.array([float(i) for i in coord[-7].strip().split()[2:]])
    H2 = np.array([float(i) for i in coord[-8].strip().split()[2:]]) 
    A, B = H1 - azote, H2 - azote
    center, r = circumcircle(A, B)            
    # calculate the vector perpendicular to the plane of the oxygen atoms
    Z = center-azote
    Z= Z / np.linalg.norm(Z)           
    # Rotate the oxygens atoms around the nitrogen atom
    A_r = rotation_z(A, Z, theta) + azote            
    B_r = rotation_z(B, Z, theta) + azote            

    H1_r = [num for num in A_r]      
    H2_r = [num for num in B_r]                              
               
    # Write to input file for GAMESS                                    
    output_file = OUTPUT_DIR / f"aniline{iteration}.inp"            
    with open(output_file, "w") as f:                
        f.write(""""
!   File created by the GAMESS Input Deck Generator Plugin for Avogadro
 $BASIS GBASIS=N31 NGAUSS=6 $END
 $CONTRL SCFTYP=RHF RUNTYP=ENERGY MAXIT=50 AIMPAC=.TRUE. $END

 $DATA 
Title
C1
N     7.0     2.31980     0.00000     0.00060
C     6.0     0.92310     0.00000     0.00090
C     6.0     0.22690     1.20210    -0.00040
C     6.0    -1.15410     1.19850    -0.00060
C     6.0    -1.84400    -0.00000     0.00050
C     6.0    -1.15410    -1.19850     0.00180
C     6.0     0.22690    -1.20210    -0.00330
H     1.0    """+str(H1_r[0])+"""    """+str(H1_r[1])+"""    """+str(H1_r[2])+"""
H     1.0    """+str(H2_r[0])+"""    """+str(H2_r[1])+"""    """+str(H2_r[2])+"""
H     1.0     0.76510     2.13850    -0.00080
H     1.0    -1.69590     2.13270    -0.00120
H     1.0    -2.92400    -0.00000     0.00070
H     1.0    -1.69590    -2.13270     0.00260
H     1.0     0.76510    -2.13850    -0.00270
 $END""")

#defining the rotation_z function            
def rotation_z(vec, Z, angle):                        
    return np.cos(angle) * vec + np.sin(angle) * np.cross(Z,vec) +(1 - np.cos(angle))* np.dot(vec, Z) * Z            
def circumcircle(A, B):                               
    center = (A + B ) / 2                
    r = np.linalg.norm(A - center)                
    return center, r  



for i in range(1,50):            
    automation(np.pi/50*i,r"C:\Users\Public\gamess-64\inputs\aniline0.inp",i)
