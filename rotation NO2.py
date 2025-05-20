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
    azote = np.array([2.09700,0.00000,0.00090])
    O1 = np.array([float(i) for i in coord[-15].strip().split()[2:]])
    O2 = np.array([float(i) for i in coord[-16].strip().split()[2:]]) 
    A, B = O1 - azote, O2 - azote
    center, r = circumcircle(A, B)            
    # calculate the vector perpendicular to the plane of the oxygen atoms
    Z = center-azote
    Z= Z / np.linalg.norm(Z)           
    # Rotate the oxygens atoms around the nitrogen atom
    A_r = rotation_z(A, Z, theta) + azote            
    B_r = rotation_z(B, Z, theta) + azote            

    O1_r = [num for num in A_r]      
    O2_r = [num for num in B_r]                              
               
    # Write to input file for GAMESS                                    
    output_file = OUTPUT_DIR / f"4nitroaniline{iteration}.inp"            
    with open(output_file, "w") as f:                
        f.write(""""
 !   File created by the GAMESS Input Deck Generator Plugin for Avogadro
 $BASIS GBASIS=N311 NGAUSS=6 NDFUNC=1 NPFUNC=1 DIFFSP=.TRUE. DIFFS=.TRUE. $END
 $CONTRL SCFTYP=RHF RUNTYP=ENERGY AIMPAC=.TRUE. $END

 $DATA 
Title
C1
N     7.0     2.09700     0.00000     0.00090
O     8.0     """+str(O1_r[0])+"""    """+str(O1_r[1])+"""    """+str(O1_r[2])+"""
O     8.0     """+str(O2_r[0])+"""    """+str(O2_r[1])+"""    """+str(O2_r[2])+"""
C     6.0     0.61700     0.00000    -0.00000
C     6.0    -0.07290    -1.19850    -0.00020
C     6.0    -1.45390    -1.20210    -0.00060
C     6.0    -2.15000     0.00000    -0.00080
C     6.0    -1.45390     1.20210    -0.00060
N     7.0    -3.54680    -0.00000    -0.00070
C     6.0    -0.07290     1.19850     0.00510
H     1.0     0.46900    -2.13270    -0.00050
H     1.0    -1.99210    -2.13850    -0.00110
H     1.0    -4.03180    -0.84000    -0.00050
H     1.0    -4.03180     0.84000    -0.00080
H     1.0    -1.99210     2.13850    -0.00070
H     1.0     0.46900     2.13270     0.00530
 $END""")

#defining the rotation_z function            
def rotation_z(vec, Z, angle):                        
    return np.cos(angle) * vec + np.sin(angle) * np.cross(Z,vec) +(1 - np.cos(angle))* np.dot(vec, Z) * Z            
def circumcircle(A, B):                               
    center = (A + B ) / 2                
    r = np.linalg.norm(A - center)                
    return center, r  



for i in range(1,50):            
    automation(np.pi/50*i,r"C:\Users\Public\gamess-64\inputs\4nitroaniline.inp",i)
