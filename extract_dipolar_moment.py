import numpy as np
import subprocess
import os
import re
import matplotlib.pyplot as plt

def extract_dipole_moment(log_files):
    dipole_moments = []
    efield_values = []
    
    for log_file in log_files:
        with open(log_file, "r") as file:
            content = file.readlines()
        
        efield_value = float(log_file.split("_E")[1].split(".log")[0])
        efield_values.append(efield_value)
        
        for i, line in enumerate(content):
            if "DX" in line and "DY" in line:
                dipole_moment = float(content[i+1].split()[-1])
                dipole_moments.append(dipole_moment)
                break
    
    return np.array(efield_values), np.array(dipole_moments)

def extract_energy_values(log_files):
    energy_values = []
    efield_values = []
    
    for log_file in log_files:
        with open(log_file, "r") as file:
            content = file.readlines()
        
        efield_value = float(log_file.split("_E")[1].split(".log")[0])
        efield_values.append(efield_value)
        
        for i, line in enumerate(content):
            if "TOTAL ENERGY =" in line:
                energy_value = float(content[i].split()[-1])
                energy_values.append(energy_value)
                break
    
    return np.array(efield_values), np.array(energy_values)

def plot_dipole_vs_efield(efield_values, dipole_moments):
    plt.figure()
    plt.plot(efield_values, dipole_moments, marker='o', linestyle='-')
    plt.xlabel("Electric Field E0 (a.u.)")
    plt.ylabel("Dipole Moment D (Debye)")
    plt.title("Dipole Moment vs. Electric Field")
    plt.grid()
    plt.savefig(dpi=300, fname="dipole_vs_efield.png")

def plot_energy_vs_efield(efield_values, energy_values):
    plt.figure()
    plt.plot(efield_values, energy_values, marker='o', linestyle='-')
    plt.xlabel("Electric Field E0 (a.u.)")
    plt.ylabel("Energy (Hartree)")
    plt.title("Energy vs. Electric Field")
    plt.grid()
    plt.savefig(dpi=300, fname="energy_vs_efield.png")

ef_values = np.linspace(0.04, 0.06, 10)
base_filename =os.path.join(os.getcwd(), "4nitroaniline")
input_files = []
for i, efield in enumerate(ef_values, start=1):
    filename = f"{base_filename}_E{efield:.6f}.inp"
    input_files.append(filename)
    print(filename)

#run_gamess_calculations(input_files)
log_files = [file.replace(".inp", ".log") for file in input_files]
ef_values, dipole_moments = extract_dipole_moment(log_files)
ef_values, energy_values = extract_energy_values(log_files)
np.savetxt("dipole_moments.txt", np.column_stack((ef_values, energy_values, dipole_moments)), delimiter="\t", header="E0 (a.u.)\tDipole Moment (Debye)")
plot_dipole_vs_efield(ef_values, dipole_moments)
plot_energy_vs_efield(ef_values, energy_values)