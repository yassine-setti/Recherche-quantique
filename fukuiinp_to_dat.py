# automatising the process of running a gamess input file
# importing the required modules
import os  
import subprocess 
import shutil

# Change directory to the desired path
os.chdir(r"C:\Users\Public\gamess-64")  
d={1:'N',2:'N2',3:'N-1'}
gamess_batch = r"C:\Users\Public\gamess-64\rungms.bat"
#i want to run gamess with the input file using subprocess and os               
for i in range(2,50):
    for j in d:
        input_file = f"inputs\\4nitroaniline{i}\\{d[j]}.inp"
            #problem : doesnt run N+1 file
        command = [gamess_batch, input_file, "2023.R1.intel", "4"]
            # Run the GAMESS process
        print(f"Running GAMESS for {input_file}...")
        subprocess.run(command, shell=True, check=True)
    #put new dat files in a folder in the restart folder
    os.rename(r"C:\Users\Public\gamess-64\restart"+f'\\N2.dat',r"C:\Users\Public\gamess-64\restart"+f'\\N+1.dat')
    os.mkdir(r"C:\Users\Public\gamess-64\restart"+f'\\4nitroaniline{i}')
    shutil.move(r"C:\Users\Public\gamess-64\restart"+f'\\N-1.dat',r"C:\Users\Public\gamess-64\restart"+f'\\4nitroaniline{i}')
    shutil.move(r"C:\Users\Public\gamess-64\restart"+f'\\N.dat',r"C:\Users\Public\gamess-64\restart"+f'\\4nitroaniline{i}')
    shutil.move(r"C:\Users\Public\gamess-64\restart"+f'\\N+1.dat',r"C:\Users\Public\gamess-64\restart"+f'\\4nitroaniline{i}')           
    if os.path.exists(fr"C:\Users\Public\gamess-64\restart\4nitroaniline{i}.dat"):
        print("The output file is created")
 