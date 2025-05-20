#from an inp file , i want to create three similar ones and put them in an associated folder    
import numpy as np
import re
import os
import subprocess
import shutil   
from pathlib import Path    
from PIL import ImageGrab   
import pyautogui    
import time 
import matplotlib.pyplot as plt

def fukui_inp_generator(file_path,i):
    #reading the file
    with open(file_path+f'\\4nitroaniline{i}.inp', 'r') as f:
        lines = f.readlines()
        #rename the file to 4nitroanilineN.inp        
    os.rename(file_path+f'\\4nitroaniline{i}.inp', file_path+f'\\N.inp')                    
        
    with open(file_path+f'\\N-1.inp', 'w') as f:

        for line in lines:
            if line ==' $CONTRL SCFTYP=RHF RUNTYP=ENERGY AIMPAC=.TRUE. ICHARG=0 MULT=1 $END\n':
                f.write(' $CONTRL SCFTYP=UHF RUNTYP=ENERGY AIMPAC=.TRUE. ICHARG=1 MULT=2 $END\n')
            else:    
                f.write(line)
    with open(file_path+f'\\N2.inp', 'w') as f:

        for line in lines:
            if line ==' $CONTRL SCFTYP=RHF RUNTYP=ENERGY AIMPAC=.TRUE. ICHARG=0 MULT=1 $END\n':
                f.write(' $CONTRL SCFTYP=UHF RUNTYP=ENERGY AIMPAC=.TRUE. ICHARG=-1 MULT=2 $END\n')
            else:    
                f.write(line)   

    #create a folder in the file path and put these three files into that folder                     
    os.mkdir(file_path+f'\\4nitroaniline{i}')
    shutil.move(file_path+f'\\N-1.inp',file_path+f'\\4nitroaniline{i}')
    shutil.move(file_path+f'\\N.inp',file_path+f'\\4nitroaniline{i}')
    shutil.move(file_path+f'\\N2.inp',file_path+f'\\4nitroaniline{i}')
    return f"3 files created for 4nitroaniline{i}N"

for i in range(1,50):
    fukui_inp_generator(r"C:\Users\Public\gamess-64\inputs",i)

    