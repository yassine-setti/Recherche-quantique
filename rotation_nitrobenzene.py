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
    azote = np.array([1.65460,0.00000,0.00100])
    O1 = np.array([float(i) for i in coord[-13].strip().split()[2:]])
    O2 = np.array([float(i) for i in coord[-14].strip().split()[2:]]) 
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
    output_file = OUTPUT_DIR / f"nitrobenzene{iteration}.inp"            
    with open(output_file, "w") as f:                
        f.write(""""
!   File created by the GAMESS Input Deck Generator Plugin for Avogadro
 $BASIS GBASIS=N31 NGAUSS=6 $END
 $CONTRL SCFTYP=RHF MAXIT=50 AIMPAC=.TRUE. $END

 $DATA 
Title
C1
N     7.0     1.65460     0.00000     0.00100
O     8.0     """+str(O1_r[0])+"""    """+str(O1_r[1])+"""    """+str(O1_r[2])+"""
O     8.0     """+str(O2_r[0])+"""    """+str(O2_r[1])+"""    """+str(O2_r[2])+"""
C     6.0     0.17440     0.00000     0.00000
C     6.0    -0.51680    -1.19710    -0.00010
C     6.0    -1.89910    -1.19710    -0.00100
C     6.0    -2.59030    -0.00000    -0.00140
C     6.0    -1.89910     1.19710    -0.00040
C     6.0    -0.51680     1.19710     0.00490
H     1.0     0.02320    -2.13250     0.00020
H     1.0    -2.43910    -2.13250    -0.00180
H     1.0    -3.67030    -0.00000    -0.00280
H     1.0    -2.43910     2.13250    -0.00110
H     1.0     0.02320     2.13240     0.00570
 $END""")

#defining the rotation_z function            
def rotation_z(vec, Z, angle):                        
    return np.cos(angle) * vec + np.sin(angle) * np.cross(Z,vec) +(1 - np.cos(angle))* np.dot(vec, Z) * Z            
def circumcircle(A, B):                               
    center = (A + B ) / 2                
    r = np.linalg.norm(A - center)                
    return center, r  



for i in range(1,50):            
    automation(np.pi/50*i,r"C:\Users\Public\gamess-64\inputs\nitrobenzene0.inp",i)
