import numpy as np
import subprocess
import os

def generate_orca_inputs(base_filename, efield_values):
    template = """ # Advanced Mode
# 
! B3LYP RHF 6-311++G(d,p) NormalPrint VeryTightSCF 
%scf
	MaxIter 125
	CNVDIIS 1
	CNVSOSCF 1
	EField {:.6f}, 0.0, 0.0 # x, y, z components (in au) of the electric field
end

%output
	print[p_mos] true
	print[p_basis] 5
end

%MaxCore 4000

* xyz 0 1
O    -2.68900    -1.05000    -0.00900
O    -2.68900    1.05000    -0.00200
N    -2.13600    0.00000    -0.00400
N    3.45500    -0.00000    0.00800
C    -0.68700    0.00000    -0.00100
C    2.09800    -0.00000    0.00500
C    0.00200    -1.20600    -0.00400
C    0.00200    1.20600    0.00400
C    1.38000    -1.20800    -0.00100
C    1.38000    1.20800    0.00700
H    -0.54800    -2.13400    -0.00800
H    -0.54800    2.13400    0.00600
H    1.91400    -2.14900    -0.00200
H    1.91400    2.14900    0.01100
H    3.96800    -0.85300    0.00200
H    3.96800    0.85300    0.00700
*
"""
    
    input_files = []
    for i, efield in enumerate(efield_values, start=1):
        if not os.path.exists(f"E{efield:.6f}"):
            os.makedirs(f"E{efield:.6f}")
        filename = f"E{efield:.6f}/{base_filename}_E{efield:.6f}_orca.inp"
        with open(filename, "w") as file:
            file.write(template.format(efield))
        input_files.append(filename)
        print(f"Generated: {filename}")
    return input_files

def run_orca_calculations(input_files):
    for filename in input_files:
        output_filename = filename.replace(".inp", ".log")
        command = ["orca", filename]
        print(f"Running: {' '.join(command)}")
        with open(output_filename, "w") as output_file:
            subprocess.run(command, stdout=output_file, stderr=subprocess.STDOUT)

ef_values = np.array([0.043250,0.043450,0.043550,0.043750])
input_files = generate_orca_inputs("4nitroaniline", ef_values)
run_orca_calculations(input_files)
