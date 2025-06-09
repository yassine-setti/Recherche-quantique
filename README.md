Recherche-quantique
Project P005: Quantum Crystallography

User Guide for Python Programs
Programs: Autoscreen.py and Autoscreen_nitroaniline.py
Goal
These programs provide an interface that automates sequences of MultiWFN commands across many input files. The interface allows quick access to various pre-implemented command sequences.

Their main benefit is applying identical command sequences efficiently across files and compiling the results into a video.

Installation
These programs use machine-specific file paths. To use them, you must modify the code to include the correct paths:

Path to the MultiWFN executable (in the MultiWFN_exe function)

Path to the folder containing the .wfn files

Any paths used in the command sequences (e.g., for subtracting electron density)

Once set, run the program and adjust numerical values in the interface as needed.

Usage
When launched, the interface displays pre-implemented MultiWFN options and a section for custom commands.

Each option is in an orange box, and the salmon-colored button executes the program based on values in the white fields. Buttons include illustrations. The top-left box shows the progress bar. A "Quit" button exits the program.

Custom Commands
For custom inputs, enter commands in this format:
['X', 'Y', …]
where X, Y, etc., are strings for the MultiWFN command prompt.

Example:
commands = ['4', '1', '2', '200,200', '1', '0.2', '0', 'q']
Then click the “Execute” button.

Subtraction of Electronic Density
To compute electron density differences:

Update the file path to the .wfn file that will be subtracted

Set the desired isovalue for the graph

Modify the command sequence in commands_densite if needed

Click the button to apply it to all .wfn files in the folder

A video of the generated images will be created in the directory set in commands_densite_func.

Orbitals
Specify the desired orbital number (by ascending energy) and the isovalue in the dedicated interface fields.
The program runs the command sequence for all .wfn files and creates a video in the directory set by commands_orbitale_func.

Electron Densities on an Interbasin Path
Using paths from chemindensite, the program calculates electron density for each .wfn file along predefined paths.
At the end, a video is created from all generated images in the directory specified in commands_surface_densitechemin_func.

Atomic Basin Surfaces
The "Atomic Basin Surfaces" option allows visualizing atomic basins from each .wfn file through the MultiWFN menu.
No video is generated; users must take screenshots manually.

Raman Intensity
Important: This requires a .out file with vibrational data from a GAMESS or Orca calculation.
This option plots the Raman intensity curve vs. vibrational frequency. No additional configuration is needed if .out files are ready.

Program: video.py
This script searches a given folder for images starting with "disl" (the default prefix for MultiWFN output images).
It uses the create_video_from_images function to make a video and deletes the images afterward.

It is used by Autoscreen.py to compile results into videos.

Program: generate_orca.py
This script examines how an electric field (E) influences a molecular system.

Initialization
You must enter the atomic coordinates of the molecule in the defined Orca file header, without changing the header itself.
Then, define the energy values to study by modifying the ef_values list.

Functionality
The program creates a new folder for each energy value and places a .inp file in each.
It runs Orca calculations and stores the results in the corresponding folders.

Program: rotation.py
Goal
This script generates files by rotating one group within a molecule.

Installation
To set up:

Provide valid file paths

Input a .inp file with the molecule

Modify atom coordinates accordingly to match your molecule’s geometry and header

Functionality
The program starts from the initial geometry and calculates atomic positions for rotated configurations.
For any input angle θ, it creates a .inp file with the group rotated by θ.
To simulate multiple rotations, loop over a range of angles.

Each rotation generates a file in the script directory, numbered according to the angle index.
